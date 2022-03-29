import { PlatformConfig } from 'homebridge';

/**
 * This is the name of the platform that users will use to register the plugin in the Homebridge config.json
 */
export const PLATFORM_NAME = 'AnishmgoyalThermostatHomebridgePlugin';

/**
 * This must match the name of your plugin as defined the package.json
 */
export const PLUGIN_NAME = '@anishmgoyal/homebridge-thermostat-plugin';

// BEGIN configuration type definitions

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export interface ThermostatConfig extends Record<string, any> {
    displayName: string;
    hostname: string;
}

export interface ThermostatPlatformConfig extends PlatformConfig {
    thermostats: ThermostatConfig[];
}
