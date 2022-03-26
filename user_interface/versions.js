function createVersionManager() {
    const currVersionUrl = `${systemRoot}/head`;
    const updateUrl = `${systemRoot}/update`;

    let overlayRef = null;
    function createOverlay() {
        closeOverlay(); // Make sure there isn't already an overlay

        const content = `
            <div class="versions-update-overlay">
                <div class="versions-update-message">
                    Applying update
                </div>
            </div>
        `;

        overlayRef = document.createElement('div');
        overlayRef.innerHTML = content;
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
                window.location.reload();
            } catch (e) {
                console.error('Failed to run update.');
                if (sub != null) {
                    sub.unsubscribe();
                }
            } finally {
                closeOverlay(); // Make sure we close the overlay either way
            }
        }
    };
}

const versionManager = createVersionManager();
