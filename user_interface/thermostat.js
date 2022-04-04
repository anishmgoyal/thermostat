const DEG = '&deg;';

function createExternalSensorDiv(displayName, tempC) {
    const elem = document.createElement('div');
    elem.classList.add('temperature-panel-secondary');

    const header = document.createElement('div');
    header.classList.add('temperature-panel-item-header', 'text-secondary');
    header.innerText = displayName;

    const tempDiv = document.createElement('div');
    tempDiv.classList.add('temperature-panel-item-body');
    updateTempDivWithFahrenheit(tempDiv, tempC);

    elem.appendChild(header);
    elem.appendChild(tempDiv);

    return {elem, tempDiv};
}

function updateTempDivWithFahrenheit(tempElem, tempC) {
    const tempF = tempC * 9 / 5 + 32;
    tempElem.innerHTML = `${tempF.toFixed(0)}${DEG}F`;
}

window.addEventListener('load', () => {
    const tempPanel = document.getElementById('temp-panel');
    const mainTempGridBlock = document.getElementById('main-temp-block');
    const mainTemp = document.getElementById('main-temp');
    const externalTempSensors = new Map();

    const currTimeElem = document.getElementById('curr-time');
    const currDateElem = document.getElementById('curr-date');
    const coolingControl = createTempControl('cooling-control');
    const heatingControl = createTempControl('heating-control');

    const heatButton = createHeaderBarButton('heat-activation-button');
    const coolButton = createHeaderBarButton('cool-activation-button');
    const fanButton = createHeaderBarButton('fan-activation-button');
    const schedButton = createHeaderBarButton('sched-activation-button');
    const settingsButton = createHeaderBarButton('settings-button');

    const component = {
        addExternalSensor(id, displayName, tempC) {
            if (externalTempSensors.has(id)) {
                return this.updateExternalSensor(id, tempC);
            }

            const existingSensors = Array.from(externalTempSensors.values());
            existingSensors.sort((a, b) =>
                a.displayName.localeCompare(b.displayName));
            
            const beforeTarget = existingSensors.find(sensor =>
                displayName.localeCompare(sensor.displayName) < 0)?.elem;

            const {elem, tempDiv} = createExternalSensorDiv(displayName, tempC);
            externalTempSensors.set(id, {displayName, elem, tempDiv, tempC});

            tempPanel.insertBefore(elem, beforeTarget);

            if (externalTempSensors.size > 3) {
                mainTempGridBlock.classList.add('has-four-plus-sensors');
            }
            mainTempGridBlock.classList.remove('has-no-sensors');
        },
        registerInterval(callback, time) {
            callback.call(this);
            setInterval(callback.bind(this), time);
        },
        removeExternalSensor(id) {
            if (!externalTempSensors.has(id)) {
                return;
            }
            externalTempSensors.get(id).elem.remove();
            externalTempSensors.delete(id);

            if (externalTempSensors.size < 4) {
                mainTempGridBlock.classList.remove('has-four-plus-sensors');
            }

            if (externalTempSensors.size === 0) {
                mainTempGridBlock.classList.add('has-no-sensors');
            }
        },
        updateCurrentTemp(tempC) {
            updateTempDivWithFahrenheit(mainTemp, tempC);
        },
        updateDateTime(dateTime) {
            const timeFormat = Intl.DateTimeFormat('en-US', {
                hour: 'numeric',
                minute: 'numeric',
            });
            currTimeElem.innerText = timeFormat.format(dateTime);

            const dateFormat = Intl.DateTimeFormat('en-US', {
                weekday: 'long',
                month: 'long',
                day: 'numeric',
            });
            currDateElem.innerText = dateFormat.format(dateTime);
        },
        updateExternalSensor(id, tempC) {
            if (!externalTempSensors.has(id)) {
                return;
            }

            updateTempDivWithFahrenheit(
                externalTempSensors.get(id).tempDiv, tempC);
        },
        coolingControl,
        heatingControl,

        heatButton,
        coolButton,
        fanButton,
        schedButton,
        settingsButton,
    };

    component.registerInterval(component.updateDateTime, 1000);

    sseSubscription.filter('sensor_reading').subscribe(reading => {
        if (reading['sensor_type'] !== 'temp' ||
            reading['sensor_value'] == null) {
            // If we don't have a value, skip this iteration. If we have a value
            // that isn't temp, skip as well, we don't handle humidity / other
            // potential sensor readings.
            return;
        }

        if (reading['sensor_id'] === MAIN_TEMP_SENSOR_ID) {
            component.updateCurrentTemp(reading['sensor_value'])
        }
    });

    const baseThermostatComponent = component;
    apiRegistry.register();
    currentStateManager.register(baseThermostatComponent);
    menuComponent.register(baseThermostatComponent);
    runDataManager.register(baseThermostatComponent);
});

const createTempControl = function(baseId) {
    const control = document.getElementById(baseId);
    const minusControl = document.getElementById(`${baseId}-minus`);
    const plusControl = document.getElementById(`${baseId}-plus`);
    const valueElem = document.getElementById(`${baseId}-value`);
    return {
        hideControl() {
            control.style.visibility = 'hidden';
        },
        showControl() {
            control.style.visibility = 'visible';
        },
        setVisible(visible) {
            if (!visible) {
                this.hideControl();
            } else {
                this.showControl();
            }
        },
        updateValue(value) {
            updateTempDivWithFahrenheit(valueElem, value);
        },
        minusControl,
        plusControl,
    };
}

function createHeaderBarButton(id) {
    const button = document.getElementById(id);
    button.classList.add('disabled-function');
    let isActive = false;
    let isEnabled = false;

    return {
        button,
        activate() {
            isActive = true;
            button.classList.add('activated-function');
        },
        deactivate() {
            isActive = false;
            button.classList.remove('activated-function');
        },
        setActive(_isActive) {
            if (_isActive) {
                this.activate();
            } else {
                this.deactivate();
            }
        },
        isActive() {
            return isActive;
        },

        enable() {
            isEnabled = true;
            button.classList.remove('disabled-function');
        },
        disable() {
            isEnabled = false;
            button.classList.add('disabled-function');
        },
        setEnabled(_isEnabled) {
            if (_isEnabled) {
                this.enable();
            } else {
                this.disable();
            }
        },
        isEnabled() {
            return isEnabled;
        },
    }
}

// Add a cursor override for development
window.addEventListener('keypress', ev => {
    if (ev.key === 'c') {
        document.body.style.cursor = 'auto';
    }
});

if (LOCAL_DEV_MODE) {
    document.body.style.cursor = 'auto';
}
