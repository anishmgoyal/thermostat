const apiRoot = '/api';       // Root for main API
const systemRoot = '/system'; // Root for system update module

const [BEHAVE_HOLD, BEHAVE_SCHED] = [0, 1];
const ALL_BEHAVIORS = new Set([BEHAVE_HOLD, BEHAVE_SCHED]);

const [MODE_OFF, MODE_COOL, MODE_HEAT, MODE_AUTO] = [0, 1, 2, 3];
const ALL_MODES = new Set([MODE_OFF, MODE_COOL, MODE_HEAT, MODE_AUTO]);

const DISPLAY_FAHREN = 'f';
const DISPLAY_CELSIUS = 'c';
const ALL_DISPLAY_UNITS = new Set([DISPLAY_FAHREN, DISPLAY_CELSIUS]);

const MIN_ALLOWED_TEMP_DIFF = 2.2222;

const MAIN_TEMP_SENSOR_ID = 'amg_thermostat_main';

const LOCAL_DEV_MODE = true;
