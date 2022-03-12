function createGenericApiManager(configType, subfolder, props = {}) {
    const url = `${apiRoot}/${subfolder}`;
    const updateEvents = sseSubscription.onConfigUpdate(configType).map(
        value => {
            console.log(`Update event received for ${configType}`);
            return value;
        },
    );

    const manager = {
        snapshot: null,
        onUpdate: createSubscriptionNode(),
        async reload() {
            console.log(`Reloading ${configType}`);
            const rawData = await fetch(url);
            const data = await rawData.json();
            this.snapshot = data;
            this.onUpdate.dispatch(data);
            return data;
        },
        update(newValue) {
            return fetch(url, {
                body: JSON.stringify(newValue),
                headers: {
                    'Content-Type': 'application/json',
                },
                method: 'POST',
            });
        },
        ...props,
    };

    updateEvents.subscribe(() => manager.reload());
    manager.reload();
    return manager;
}
