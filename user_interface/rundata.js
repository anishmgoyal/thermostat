const runDataManager = createGenericApiManager('rundata', 'run_data', {
    register(thermostatComponent) {
        runDataHelpers.registerTempControl(thermostatComponent.coolingControl,
            'target_cool_temp');
        runDataHelpers.registerTempControl(thermostatComponent.heatingControl,
            'target_heat_temp');

        runDataHelpers.registerSystemButton(thermostatComponent);
        runDataHelpers.registerFanButton(thermostatComponent);

        this.onUpdate.subscribe(runData => {
            runDataHelpers.applyToUI(thermostatComponent, runData);
        });
    }
});

// Helper functions
const runDataHelpers = {
    applyToUI(thermostatComponent, runData) {
        const modeStr = {
            [MODE_OFF]: 'Off',
            [MODE_COOL]: 'Cool',
            [MODE_HEAT]: 'Heat',
            [MODE_AUTO]: 'Auto',
        }[runData['active_mode']];
    
        const modeClass = `text-${labelToClassName(modeStr)}`;
        thermostatComponent.systemButton.updateValue(modeStr, modeClass);

        const [showHeat, showCool] = {
            [MODE_OFF]: [false, false],
            [MODE_COOL]: [false, true],
            [MODE_HEAT]: [true, false],
            [MODE_AUTO]: [true, true],
        }[runData['active_mode']];
        thermostatComponent.heatingControl.setVisible(showHeat);
        thermostatComponent.coolingControl.setVisible(showCool);

        // TODO: Disable the plus / minus button if it would make the temp
        // diff between heat and cool too small
    
        const fanStr = {
            true: 'On',
            false: 'Auto',
        }[runData['fan_enabled']];
    
        const fanClass = `text-${labelToClassName(fanStr)}`;
        thermostatComponent.fanButton.updateValue(fanStr, fanClass);
    
        const behaviorStr = {
            [BEHAVE_HOLD]: 'Hold',
            [BEHAVE_SCHED]: 'Schedule',
        }[runData['behavior']];
    
        const behaviorClass = `text-${labelToClassName(behaviorStr)}`;
        thermostatComponent.modeButton.updateValue(
            behaviorStr, behaviorClass);
    
        const appliedSettings = runData['settings'][runData['active_mode']];
        const targetHeat = appliedSettings?.['target_heat_temp'];
        if (targetHeat != null) {
            thermostatComponent.heatingControl.updateValue(targetHeat);
        }
    
        const targetCool = appliedSettings?.['target_cool_temp'];
        if (targetCool != null) {
            thermostatComponent.coolingControl.updateValue(targetCool);
        }
    },

    doTempChange(key, multiplier) {
        if (runDataManager.isUpdating) { // Don't change a stale copy
            return;
        }

        const runData = runDataManager.getWorkingCopy();
        const activeMode = runData['active_mode'];
        if (activeMode === MODE_OFF) {
            return; // Mode 'off' is always null
        }

        const units = configManager.snapshot['display_units'];
        const increment = units === DISPLAY_CELSIUS ? 1 : 5/9;
        const changeAmount = increment * multiplier;

        const settingsToChange =
            runData['settings'][activeMode];
        if (settingsToChange?.hasOwnProperty(key)) {
            settingsToChange[key] += changeAmount;
        }
        runDataManager.update(runData);
    },

    registerTempControl(tempControl, key) {
        tempControl.minusControl.addEventListener(
            'click', () => runDataHelpers.doTempChange(key, -1));
        tempControl.plusControl.addEventListener(
            'click', () => runDataHelpers.doTempChange(key, +1));
    },

    registerSystemButton(thermostatComponent) {
        thermostatComponent.systemButton.button.addEventListener('click', () => {
            if (runDataManager.isUpdating) {
                return;
            }
            
            const runData = runDataManager.getWorkingCopy();
            runData['active_mode'] =
                (runData['active_mode'] + 1) % 4;
            runDataManager.update(runData);
        });
    },

    registerFanButton(thermostatComponent) {
        thermostatComponent.fanButton.button.addEventListener('click', () => {
            if (runDataManager.isUpdating) {
                return;
            }

            const runData = runDataManager.getWorkingCopy();
            runData['fan_enabled'] =
                !runData['fan_enabled'];
            runDataManager.update(runData);
        });
    },

    registerModeButton(thermostatComponent) {
        // TODO: Add support for schedules. For now, don't let the user cycle
        // to the run schedule mode. The thermostat defaults to hold mode, which
        // is supported
    },
};