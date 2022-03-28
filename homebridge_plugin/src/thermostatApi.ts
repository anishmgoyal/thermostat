import { connect, Client } from 'mqtt';
import { Observable, Observer, of, ReplaySubject } from 'rxjs';
import { combineLatestWith, first, map, shareReplay, switchMap } from 'rxjs/operators';
import { get, IncomingMessage, request } from 'http';
import { ThermostatHomebridgePlatform } from './platform';

const MQTT_HUB_HOSTNAME = 'amgthermostathub.local';
const MQTT_TOPIC = '/house/amg_thermostat/events';
const RECONNECT_WAIT = 1000;

const THERMOSTAT_API_PORT = 8001;

const MIN_THRESHOLD_DIFF = 2.2222; // Degrees celsius, translates to 4F

/**
 * Exposes methods for getting current configuration, and providing new
 * configuration, to a running thermostat
 */
export class ThermostatApi {
  static client?: Client;

  private readonly baseUrl =
    `http://${this.hostname}.local:${THERMOSTAT_API_PORT}/api`;

  private currentTempC$ = new ReplaySubject<number>(1);
  private circuitState$ = new ReplaySubject<CircuitState>(1);
  private runData$ = new ReplaySubject<RunData>(1);

  readonly state$: Observable<ThermostatState> = this.currentTempC$.pipe(
    combineLatestWith(this.circuitState$, this.runData$),
    map(([currentTempC, circuitState, runData]) => ({
      currentTemperature: currentTempC,
      currentHeatingCoolingState: circuitState.mode,
      fanMode: runData.fan_enabled ? 'on' as const : 'auto' as const,
      fanState: circuitState.fan,
      targetHeatingCoolingState:
                RUN_DATA_MODE_TO_STR[runData.active_mode],
      targetTemperature:
                runData.active_mode === ThermostatMode.COOL ?
                  runData.settings[runData.active_mode].target_cool_temp :
                  runData.active_mode === ThermostatMode.HEAT ?
                    runData.settings[runData.active_mode].target_heat_temp :
                    undefined,
      coolingThresholdTemperature:
                runData.settings[runData.active_mode]?.target_cool_temp,
      heatingThresholdTemperature:
                runData.settings[runData.active_mode]?.target_heat_temp,
    })),
    shareReplay(1),
  );

  constructor(private readonly platform: ThermostatHomebridgePlatform,
              private readonly hostname: string) {
    if (ThermostatApi.client == null) {
      ThermostatApi.subscribeToMqtt();
    }

    ThermostatApi.client?.on('message', (_topic, message) => {
      this.processMQTTEvent(JSON.parse(message.toString()));
    });

    this.getCircuitState().pipe(first()).subscribe(
      circuitState => this.circuitState$.next(circuitState));
    this.getRunData().pipe(first()).subscribe(
      runData => this.runData$.next(runData));
  }

  setFanState(state: 'on' | 'auto') {
    return this.getRunData().pipe(
      first(),
      switchMap(runData => {
        runData.fan_enabled = state === 'on';
        return this.setRunData(runData);
      }));
  }

  setTargetHeatingCoolingState(state: 'off' | 'cool' | 'heat' | 'auto') {
    return this.getRunData().pipe(
      first(),
      switchMap(runData => {
        runData.active_mode = STR_MODE_TO_RUN_DATA[state];
        return this.setRunData(runData);
      }));
  }

  setTargetTemperature(tempC: number) {
    return this.getRunData().pipe(
      first(),
      switchMap(runData => {
        switch (runData.active_mode) {
          case ThermostatMode.OFF:
          case ThermostatMode.AUTO:
            // Don't do anything here - we can't set a target temp
            // if we're off, or if we're in auto mode
            return of('');
          case ThermostatMode.COOL:
            runData.settings[ThermostatMode.COOL]
              .target_cool_temp = tempC;
            break;
          case ThermostatMode.HEAT:
            runData.settings[ThermostatMode.HEAT]
              .target_heat_temp = tempC;
            break;
        }
        return this.setRunData(runData);
      }));
  }

  setCoolingThresholdTemp(tempC: number) {
    return this.getRunData().pipe(
      first(),
      switchMap(runData => {
        if (runData.active_mode === ThermostatMode.OFF ||
                    runData.active_mode === ThermostatMode.HEAT) {
          return of('');
        }

        if (runData.active_mode === ThermostatMode.AUTO) {
          tempC = Math.max(
            tempC,
            runData.settings[runData.active_mode].target_heat_temp +
              MIN_THRESHOLD_DIFF);
        }

        if (tempC === runData.settings[runData.active_mode].target_cool_temp) {
          return of(''); // no-op
        }

        runData.settings[runData.active_mode].target_cool_temp = tempC;
        return this.setRunData(runData);
      }));
  }

  setHeatingThresholdTemp(tempC: number) {
    return this.getRunData().pipe(
      first(),
      switchMap(runData => {
        if (runData.active_mode === ThermostatMode.OFF ||
                    runData.active_mode === ThermostatMode.COOL) {
          return of('');
        }

        if (runData.active_mode === ThermostatMode.AUTO) {
          tempC = Math.min(
            tempC,
            runData.settings[runData.active_mode].target_cool_temp -
              MIN_THRESHOLD_DIFF);
        }

        if (tempC === runData.settings[runData.active_mode].target_heat_temp) {
          return of(''); // no-op
        }

        runData.settings[runData.active_mode].target_heat_temp = tempC;
        return this.setRunData(runData);
      }),
    );
  }

  private getCircuitState(): Observable<CircuitState> {
    return ThermostatApi.sendGetRequest(`${this.baseUrl}/current_state`)
      .pipe(map(rawState => JSON.parse(rawState)));
  }

  private getRunData(): Observable<RunData> {
    return ThermostatApi.sendGetRequest(`${this.baseUrl}/run_data`)
      .pipe(map(rawRunData => JSON.parse(rawRunData)));
  }

  private processMQTTEvent(event: ThermostatEvent) {
    if (event.event_type === 'update_configuration') {
      if (event.config_type === 'rundata') {
        this.getRunData().pipe(first()).subscribe(
          runData => this.runData$.next(runData));
      }
    } else if (event.event_type === 'sensor_reading') {
      if (event.sensor_id === MAIN_SENSOR_ID &&
                event.sensor_type === 'temp') {
        this.currentTempC$.next(event.sensor_value);
      }
    } else if (event.event_type === 'status_change') {
      if (event.hostname !== this.hostname) {
        return;
      }
      this.circuitState$.next({ fan: event.fan, mode: event.mode });
    }
  }

  private setRunData(runData: RunData): Observable<string> {
    return ThermostatApi.sendPostRequest(
      this.platform,
      `${this.baseUrl}/run_data`,
      JSON.stringify(runData),
      'application/json',
    );
  }

  private static readHttpMessage(
    observer: Observer<string>,
    res: IncomingMessage,
    method: string,
    url: string) {
    if (Math.floor((res.statusCode ?? 0) / 100) !== 2) {
      const msg = `Failed to make ${method} request to ${url}: ` +
                `${res.statusCode} ${res.statusMessage}`;
      observer.error(new Error(msg));
      res.resume();
      return;
    }

    const chunks: string[] = [];
    res.setEncoding('utf8');
    res.on('data', chunk => chunks.push(chunk));
    res.on('end', () => {
      observer.next(chunks.join());
      observer.complete();
    });
  }

  private static sendGetRequest(url: string): Observable<string> {
    return new Observable(observer => {
      get(url, (res) => {
        this.readHttpMessage(observer, res, 'GET', url);
      }).on('error', (err) => {
        observer.error(err);
      });
    });
  }

  private static sendPostRequest(
    platform: ThermostatHomebridgePlatform,
    url: string,
    body: string,
    mimetype?: string,
  ): Observable<string> {
    platform.log.debug(`Write ${JSON.stringify(body)} to ${url}`);
    return new Observable(observer => {
      const req = request(url, {
        method: 'POST',
        headers: {
          'Content-Type': mimetype ?? 'text/plain',
        },
      }, (res) => {
        this.readHttpMessage(observer, res, 'POST', url);
      });
      req.on('error', (err) => {
        observer.error(err);
      });
      req.write(body);
      req.end();
    });
  }

  private static subscribeToMqtt() {
    this.client = connect(`mqtt://${MQTT_HUB_HOSTNAME}`);
    this.client.on('connect', () => {
      this.client?.subscribe(MQTT_TOPIC);
    });
    this.client.on('error', () => {
      if (this.client?.disconnected && !this.client?.reconnecting) {
        setTimeout(() => this.client?.reconnect(), RECONNECT_WAIT);
      }
    });
  }
}

// Exposed states

export interface ThermostatState {
    currentHeatingCoolingState: 'off' | 'cool' | 'heat';
    fanMode: 'on' | 'auto'; // The set mode (what the user selected)
    fanState: 'on' | 'auto'; // The current fan circuit state
    targetHeatingCoolingState: 'off' | 'cool' | 'heat' | 'auto';
    currentTemperature: number;
    targetTemperature?: number;
    coolingThresholdTemperature?: number;
    heatingThresholdTemperature?: number;
}

// MQTT Events

type ThermostatEvent =
    ConfigUpdateEvent | StatusChangeEvent | SensorReadingEvent;

interface ConfigUpdateEvent {
    event_type: 'update_configuration';
    config_type: 'config' | 'rundata' | 'schedule';
}

interface StatusChangeEvent {
    event_type: 'status_change';
    hostname: string;
    mode: 'off' | 'heat' | 'cool';
    fan: 'on' | 'auto';
}

const MAIN_SENSOR_ID = 'amg_thermostat_main';
interface SensorReadingEvent {
    event_type: 'sensor_reading';
    sensor_id: string;
    sensor_type: 'temp' | 'humid';
    sensor_value: number;
}

// API types

interface CircuitState {
    mode: 'off' | 'cool' | 'heat';
    fan: 'on' | 'auto';
}

enum ThermostatMode {
    OFF = 0,
    COOL = 1,
    HEAT = 2,
    AUTO = 3,
}

interface RunData {
    active_mode: ThermostatMode;
    behavior: number;
    fan_enabled: boolean;
    settings: [
        // Mode off
        null,
        // Mode cool
        {
            target_cool_temp: number;
            target_heat_temp: never;
        },
        // Mode heat
        {
            target_cool_temp: never;
            target_heat_temp: number;
        },
        // Mode auto
        {
            target_cool_temp: number;
            target_heat_temp: number;
        },
    ];
}

// Convenience types
const RUN_DATA_MODE_TO_STR: {
    [key in ThermostatMode]: ThermostatState['targetHeatingCoolingState']
} = {
  [ThermostatMode.OFF]: 'off',
  [ThermostatMode.COOL]: 'cool',
  [ThermostatMode.HEAT]: 'heat',
  [ThermostatMode.AUTO]: 'auto',
};

const STR_MODE_TO_RUN_DATA: {
    [key in ThermostatState['targetHeatingCoolingState']]: ThermostatMode
} = {
  'off': ThermostatMode.OFF,
  'cool': ThermostatMode.COOL,
  'heat': ThermostatMode.HEAT,
  'auto': ThermostatMode.AUTO,
};
