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
        isUpdating: false,
        getWorkingCopy() {
            return JSON.parse(JSON.stringify(this.snapshot));
        },
        async reload() {
            console.log(`Reloading ${configType}`);
            this.isUpdating = true;
            try {
                const rawData = await fetch(url);
                const data = await rawData.json();
                this.snapshot = data;
                this.onUpdate.dispatch(data);
                return data;
            } catch (e) {
                return this.snapshot;
            } finally {
                this.isUpdating = false;
            }
        },
        async update(newValue) {
            this.isUpdating = true; // Keep marked as updating until we reload
            try {
                const response = await fetch(url, {
                    body: JSON.stringify(newValue),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    method: 'POST',
                });

                if (response.status % 100 !== 2) {
                    throw new Error('Error response');
                }

                return response.body;
            } catch (e) {
                this.isUpdating = false; // If we fail to update, allow changes
                return null;
            }
        },
        ...props,
    };

    updateEvents.subscribe(() => manager.reload());
    manager.reload();
    return manager;
}
