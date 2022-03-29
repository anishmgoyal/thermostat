import { API, DynamicPlatformPlugin, Logger, PlatformAccessory, Service, Characteristic, PlatformConfig } from 'homebridge';

import { PLATFORM_NAME, PLUGIN_NAME, ThermostatPlatformConfig } from './settings';
import { ThermostatPlatformAccessory } from './platformAccessory';
import { ThermostatApi } from './thermostatApi';

/**
 * ThermostatHomebridgePlatform
 * Parses user configuration for thermostats
 */
export class ThermostatHomebridgePlatform implements DynamicPlatformPlugin {
  public readonly Service: typeof Service = this.api.hap.Service;
  public readonly Characteristic: typeof Characteristic = this.api.hap.Characteristic;

  public readonly config: ThermostatPlatformConfig;

  // this is used to track restored cached accessories
  public readonly accessories: PlatformAccessory[] = [];

  constructor(
    public readonly log: Logger,
    config: PlatformConfig,
    public readonly api: API,
  ) {
    ThermostatApi.logger = this.log;

    this.config = config as ThermostatPlatformConfig;
    this.log.debug('Finished initializing platform:', this.config.name);

    // When this event is fired it means Homebridge has restored all cached accessories from disk.
    // Dynamic Platform plugins should only register new accessories after this event was fired,
    // in order to ensure they weren't added to homebridge already. This event can also be used
    // to start discovery of new accessories.
    this.api.on('didFinishLaunching', () => {
      log.debug('Executed didFinishLaunching callback');
      // run the method to discover / register your devices as accessories
      this.discoverDevices();
    });
  }

  /**
   * This function is invoked when homebridge restores cached accessories from disk at startup.
   * It should be used to setup event handlers for characteristics and update respective values.
   */
  configureAccessory(accessory: PlatformAccessory) {
    this.log.info('Loading accessory from cache:', accessory.displayName);

    // add the restored accessory to the accessories cache so we can track if it has already been registered
    this.accessories.push(accessory);
  }

  /**
   * Register thermostats enumerated in the homebridge config file
   */
  discoverDevices() {
    for (const device of this.config.thermostats) {
      const uuid = this.api.hap.uuid.generate(device.hostname);
      const existingAccessory = this.accessories.find(
        accessory => accessory.UUID === uuid);
      if (existingAccessory) {
        this.log.info('Restoring existing accessory from cache:',
          existingAccessory.displayName);
        new ThermostatPlatformAccessory(this, existingAccessory);
      } else {
        this.log.info('Adding new accessory:', device.displayName);
        const accessory = new this.api.platformAccessory(
          device.displayName, uuid);
        accessory.context.device = device;
        new ThermostatPlatformAccessory(this, accessory);
        this.api.registerPlatformAccessories(PLUGIN_NAME, PLATFORM_NAME, [accessory]);
      }
    }
  }
}
