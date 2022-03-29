import { Service, PlatformAccessory, CharacteristicValue } from 'homebridge';
import { firstValueFrom } from 'rxjs';

import { ThermostatHomebridgePlatform } from './platform';
import { ThermostatApi, ThermostatState } from './thermostatApi';

/**
 * Platform Accessory
 * An instance of this class is created for each accessory your platform registers
 * Each accessory may expose multiple services of different service types.
 */
export class ThermostatPlatformAccessory {
  private hostname: string;
  private fanService: Service;
  private thermostatService: Service;
  private api: ThermostatApi;

  // Aliases for supported characteristics
  readonly Active =
    this.platform.Characteristic.Active;
  readonly CurrentFanState =
    this.platform.Characteristic.CurrentFanState;
  readonly CurrHeatCool =
    this.platform.Characteristic.CurrentHeatingCoolingState;
  readonly TargetHeatCool =
    this.platform.Characteristic.TargetHeatingCoolingState;
  readonly CurrTemp =
    this.platform.Characteristic.CurrentTemperature;
  readonly TargetTemp =
    this.platform.Characteristic.TargetTemperature;
  readonly TempDisplayUnits =
    this.platform.Characteristic.TemperatureDisplayUnits;
  readonly CoolThresh =
    this.platform.Characteristic.CoolingThresholdTemperature;
  readonly HeatThresh =
    this.platform.Characteristic.HeatingThresholdTemperature;

  constructor(
    private readonly platform: ThermostatHomebridgePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.hostname = accessory.context.device.hostname;
    this.api = new ThermostatApi(this.platform, this.hostname);

    // Set minimal accessory properties
    this.accessory.getService(this.platform.Service.AccessoryInformation)!
      .setCharacteristic(this.platform.Characteristic.Manufacturer, 'Bland Devices')
      .setCharacteristic(this.platform.Characteristic.Model, 'Thermostat')
      .setCharacteristic(this.platform.Characteristic.SerialNumber, this.hostname);

    this.thermostatService =
      this.accessory.getService(this.platform.Service.Thermostat) ||
      this.accessory.addService(this.platform.Service.Thermostat);

    this.thermostatService.setCharacteristic(this.platform.Characteristic.Name,
      accessory.displayName);

    this.thermostatService.getCharacteristic(this.TargetHeatCool)
      .onSet(this.setTargetHeatingCoolingState.bind(this));

    this.thermostatService.getCharacteristic(this.TargetTemp)
      .onSet(this.setTargetTemperature.bind(this))
      .setProps({ minValue: 17, maxValue: 28 })
      .updateValue(17);

    this.thermostatService.getCharacteristic(this.TempDisplayUnits)
      .onGet(() => this.TempDisplayUnits.FAHRENHEIT);

    this.thermostatService.getCharacteristic(this.CoolThresh)
      .onSet(this.setCoolingThresholdTemperature.bind(this))
      .setProps({ minValue: 17, maxValue: 28 })
      .updateValue(17);

    this.thermostatService.getCharacteristic(this.HeatThresh)
      .onSet(this.setHeatingThresholdTemperature.bind(this))
      .setProps({ minValue: 17, maxValue: 28 })
      .updateValue(17);

    this.fanService =
      this.accessory.getService(this.platform.Service.Fanv2) ||
      this.accessory.addService(this.platform.Service.Fanv2);

    this.fanService.setCharacteristic(this.platform.Characteristic.Name,
      `${accessory.displayName} Fan`);

    this.fanService.getCharacteristic(this.Active)
      .onSet(this.setFanState.bind(this));

    this.api.state$.subscribe(state => this.updateCharacteristics(state));
  }

  async setFanState(value: CharacteristicValue) {
    let fanState: ThermostatState['fanState'] = 'auto';
    if (value === this.Active.ACTIVE) {
      fanState = 'on';
    }
    this.platform.log.debug(`Set fan state: ${fanState}`);
    await firstValueFrom(this.api.setFanState(fanState));
  }

  async setTargetHeatingCoolingState(value: CharacteristicValue) {
    let targetState: ThermostatState['targetHeatingCoolingState'] = 'off';
    switch (value) {
      case this.TargetHeatCool.OFF:
        targetState = 'off';
        break;
      case this.TargetHeatCool.COOL:
        targetState = 'cool';
        break;
      case this.TargetHeatCool.HEAT:
        targetState = 'heat';
        break;
      case this.TargetHeatCool.AUTO:
        targetState = 'auto';
        break;
    }
    this.platform.log.debug(`Set target heat/cool state: ${targetState}`);
    await firstValueFrom(this.api.setTargetHeatingCoolingState(targetState));
  }

  async setTargetTemperature(value: CharacteristicValue) {
    this.platform.log.debug(`Set target temperature: ${value as number}`);
    await firstValueFrom(this.api.setTargetTemperature(value as number));
  }

  async setCoolingThresholdTemperature(value: CharacteristicValue) {
    this.platform.log.debug(`Set cooling threshold: ${value as number}`);
    await firstValueFrom(this.api.setCoolingThresholdTemp(value as number));
  }

  async setHeatingThresholdTemperature(value: CharacteristicValue) {
    this.platform.log.debug(`Set heating threshold: ${value as number}`);
    await firstValueFrom(this.api.setHeatingThresholdTemp(value as number));
  }

  private updateCharacteristics(thermostatState: ThermostatState) {
    this.platform.log.debug(
      `Updating characteristics: ${JSON.stringify(thermostatState)}`);
    const currFanActive =
      thermostatState.fanMode === 'on' ?
        this.Active.ACTIVE :
        this.Active.INACTIVE;
    this.fanService.updateCharacteristic(
      this.Active, currFanActive);

    const currentFanState =
      thermostatState.fanState === 'on' ||
        thermostatState.currentHeatingCoolingState !== 'off' ?
        this.CurrentFanState.BLOWING_AIR :
        this.CurrentFanState.IDLE;
    this.fanService.updateCharacteristic(
      this.CurrentFanState, currentFanState);

    const currHeatCool = {
      'off': this.CurrHeatCool.OFF,
      'heat': this.CurrHeatCool.HEAT,
      'cool': this.CurrHeatCool.COOL,
    }[thermostatState.currentHeatingCoolingState];
    this.thermostatService.updateCharacteristic(
      this.CurrHeatCool, currHeatCool);

    const targetHeatCool = {
      'off': this.TargetHeatCool.OFF,
      'heat': this.TargetHeatCool.HEAT,
      'cool': this.TargetHeatCool.COOL,
      'auto': this.TargetHeatCool.AUTO,
    }[thermostatState.targetHeatingCoolingState];
    this.thermostatService.updateCharacteristic(
      this.TargetHeatCool, targetHeatCool);

    this.thermostatService.updateCharacteristic(
      this.CurrTemp, thermostatState.currentTemperature);

    if (thermostatState.targetTemperature != null) {
      this.thermostatService.updateCharacteristic(
        this.TargetTemp, thermostatState.targetTemperature);
    }

    if (thermostatState.coolingThresholdTemperature != null) {
      this.thermostatService.updateCharacteristic(
        this.CoolThresh, thermostatState.coolingThresholdTemperature);
    }

    if (thermostatState.heatingThresholdTemperature != null) {
      this.thermostatService.updateCharacteristic(
        this.HeatThresh, thermostatState.heatingThresholdTemperature);
    }
  }

}
