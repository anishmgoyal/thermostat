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

    const systemButton = createFooterBarButton('system-button');
    const fanButton = createFooterBarButton('fan-button');
    const modeButton = createFooterBarButton('mode-button');
    const menuButton = createFooterBarButton('menu-button');

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
        systemButton,
        fanButton,
        modeButton,
        menuButton,
    };

    component.registerInterval(component.updateDateTime, 1000);
    component.systemButton.updateValue('Heat', 'text-heating');
    component.fanButton.updateValue('Auto');

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
            control.style.display = 'none';
        },
        showControl() {
            control.style.display = '';
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

createFooterBarButton = function(id) {
    const button = document.getElementById(id);
    const valueElem =
        button.getElementsByClassName('footer-bar-button-value')?.[0] ?? null;
    let internalValueClass = '';
    return {
        button,
        updateValue(newValue, valueClass) {
            if (valueElem == null) {
                return;
            }
            if (internalValueClass) {
                valueElem.classList.remove(internalValueClass);
                internalValueClass = '';
            }
            if (valueClass) {
                valueElem.classList.add(valueClass);
                internalValueClass = valueClass;
            }
            valueElem.innerText = newValue;
        },
    }
}
