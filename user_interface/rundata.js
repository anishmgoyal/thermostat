const runDataManager = createGenericApiManager('rundata', 'run_data', {
    register(thermostatComponent) {
        runDataHelpers.registerTempControl(thermostatComponent.coolingControl,
            'target_cool_temp');
        runDataHelpers.registerTempControl(thermostatComponent.heatingControl,
            'target_heat_temp');

        runDataHelpers.registerFanButton(thermostatComponent);
        runDataHelpers.registerToggleCool(thermostatComponent);
        runDataHelpers.registerToggleHeat(thermostatComponent);

        this.onUpdate.subscribe(runData => {
            runDataHelpers.applyToUI(thermostatComponent, runData);
        });
    }
});

// Helper functions
const runDataHelpers = {
    applyToUI(thermostatComponent, runData) {
        const activeMode = runData['active_mode'];
        thermostatComponent.coolButton.setEnabled(
            [MODE_COOL, MODE_AUTO].includes(activeMode));
        thermostatComponent.heatButton.setEnabled(
            [MODE_HEAT, MODE_AUTO].includes(activeMode));
        thermostatComponent.fanButton.setEnabled(runData['fan_enabled']);

        thermostatComponent.coolingControl.setVisible(
            thermostatComponent.coolButton.isEnabled());
        thermostatComponent.heatingControl.setVisible(
            thermostatComponent.heatButton.isEnabled());

        // TODO: Disable the plus / minus button if it would make the temp
        // diff between heat and cool too small
    
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

    registerToggleCool(thermostatComponent) {
        thermostatComponent.coolButton.button.addEventListener('click', () => {
            this.updateActiveMode(thermostatComponent, MODE_COOL);
        });
    },

    registerToggleHeat(thermostatComponent) {
        thermostatComponent.heatButton.button.addEventListener('click', () => {
            this.updateActiveMode(thermostatComponent, MODE_HEAT);
        });
    },

    updateActiveMode(thermostatComponent, updateMask) {
        if (runDataManager.isUpdating) {
            return;
        }

        const runData = runDataManager.getWorkingCopy();
        let mask = 0;
        // MODE_COOL = 1, MODE_HEAT = 2, MODE_AUTO = MODE_COOL | MODE_HEAT
        if (thermostatComponent.coolButton.isEnabled()) {
            mask |= MODE_COOL;
        }
        if (thermostatComponent.heatButton.isEnabled()) {
            mask |= MODE_HEAT;
        }
        runData['active_mode'] = mask ^ updateMask;
        runDataManager.update(runData);
    },

    registerModeButton(thermostatComponent) {
        // TODO: Add support for schedules. For now, don't let the user cycle
        // to the run schedule mode. The thermostat defaults to hold mode, which
        // is supported
    },
};