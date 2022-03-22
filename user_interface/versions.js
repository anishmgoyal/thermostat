function createVersionManager() {
    const currVersionUrl = `${systemRoot}/head`;
    const updateUrl = `${systemRoot}/update`;
    return {
        async getCurrentHeadVersion() {
            const response = await fetch(currVersionUrl);
            const body = await response.json();
            return body['current_head'];
        },
        async runUpdate() {
            // TODO: Add an overlay to prevent user interaction during an
            // update

            let sub = null;
            try {
                const request = fetch(updateUrl, {
                    method: 'POST',
                });

                sub = sseSubscription.filter('consumer_init').subscribe(
                    () => {
                        window.location.reload();
                        sub.unsubscribe();
                    });

                await request;
            } catch (e) {
                console.error('Failed to run update.');
                if (sub != null) {
                    sub.unsubscribe();
                }
                return;
            }
        }
    };
}

const versionManager = createVersionManager();
