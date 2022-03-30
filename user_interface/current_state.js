function createCurrentStateManager() {
  const url = `${apiRoot}/current_state`;
  const updateEvents = sseSubscription.filter('state_change').map(
    value => {
      console.log(`Received state change`);
      return value; 
    },
  );
  // Reload configuration when re-initializing SSE, because we may have
  // missed events during connection
  const initEvents = sseSubscription.filter('consumer_init');

  let coolButton = null;
  let heatButton = null;
  let fanButton = null;

  const manager = {
    snapshot: null,
    isUpdating: false,
    register(thermostatComponent) {
      coolButton = thermostatComponent.coolButton;
      heatButton = thermostatComponent.heatButton;
      fanButton = thermostatComponent.fanButton;
    },
    async reload() {
        console.log(`Reloading state`);
        this.isUpdating = true;
        try {
            const rawData = await fetch(url);
            const data = await rawData.json();
            this.snapshot = data;
            this.handleStateChange(data);
            return data;
        } catch (e) {
            return this.snapshot;
        } finally {
            this.isUpdating = false;
        }
    },

    handleStateChange(state) {
      const {mode, fan} = state;
      const coolActive = ['cool', 'auto'].includes(mode);
      const heatActive = ['heat', 'auto'].includes(mode);
      const fanActive = fan === 'on' || coolActive || heatActive;

      coolButton?.setActive(coolActive);
      heatButton?.setActive(heatActive);
      fanButton?.setActive(fanActive);
    },
  };

  updateEvents.subscribe(newState => {
    manager.snapshot = newState;
    manager.handleStateChange(newState);
  })
  initEvents.subscribe((() => manager.reload()));

  return manager;
}

const currentStateManager = createCurrentStateManager();
