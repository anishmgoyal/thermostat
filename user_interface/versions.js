function createVersionManager() {
    const currVersionUrl = `${systemRoot}/head`;
    const updateUrl = `${systemRoot}/update`;

    let overlayRef = null;
    function createOverlay() {
        closeOverlay(); // Make sure there isn't already an overlay

        const content = `
            <div class="versions-update-overlay">
                <div class="versions-update-message">
                    Applying update. Page will reload automatically.
                </div>
                <div class="versions-update-message">
                    Tap anywhere to dismiss this message.
                </div>
            </div>
        `;

        overlayRef = document.createElement('div');
        overlayRef.innerHTML = content;
        overlayRef.addEventListener('click', closeOverlay);
        document.body.appendChild(overlayRef);
    }

    function closeOverlay() {
        if (overlayRef != null) {
            overlayRef.remove();
            overlayRef = null;
        }
    }

    return {
        async getCurrentHeadVersion() {
            const response = await fetch(currVersionUrl);
            const body = await response.json();
            return body['current_head'];
        },
        async runUpdate() {
            menuComponent.close();
            createOverlay();

            let sub = null;
            try {
                // Trigger and wait for the update to complete
                await fetch(updateUrl, {
                    method: 'POST',
                });
            } catch (e) {
                console.error('Failed to run update.');
                if (sub != null) {
                    sub.unsubscribe();
                }
                closeOverlay();
            }
        }
    };
}

const versionManager = createVersionManager();
sseSubscription.filter('consumer_init').subscribe(consumerInit => {
    const initVersion = consumerInit['service_version'];
    if (initVersion != null && initVersion !== BUILD_VER) {
        // We've detected a change in thermostat version, reload the page
        window.location.reload();
    }
});
