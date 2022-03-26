function createMenuComponent() {
    // One minute timeout for the menu component
    const MENU_COMPONENT_TIMEOUT = 1000*60*1;

    let baseElement = null;
    let content = `
        <div class="menu" id="menu-overlay">
            <div class="menu-buttons">
                <!--<button id="menu-edit-sched">Edit Schedule</button>-->
                <button id="menu-update" disabled="disabled">
                    No Update Available
                </button>
                <button id="menu-refresh">Refresh</button>
                <button id="menu-cancel">Cancel</button>
            </div>
        </div>
    `;

    function setupMenuCancelButton(menuComponent) {
        const button = document.getElementById('menu-cancel');
        button.addEventListener('click', () => menuComponent.close());
    }

    function setupRefreshButton(menuComponent) {
        const button = document.getElementById('menu-refresh');
        button.addEventListener('click', () => window.location.reload());
    }

    function setupUpdateButton(menuComponent) {
        const button = menuComponent.updateButton;
        button.addEventListener('click', () => versionManager.runUpdate());
    }

    function setupOverlay(menuComponent) {
        const overlay = document.getElementById('menu-overlay');
        overlay.addEventListener('click', event => {
            if (event.target !== overlay) {
                return;
            }

            menuComponent.close();
        });
    }

    function setUpdateButton(isEnabled, updateButton) {
        if (isEnabled) {
            updateButton.innerText = 'Update';
            updateButton.disabled = false;
        } else {
            updateButton.innerText = 'No Update Available';
            updateButton.disabled = true;
        }
    };

    async function checkForUpdates(menuComponent) {
        const ver = await versionManager.getCurrentHeadVersion();
        setUpdateButton(ver !== BUILD_VER, menuComponent.updateButton);
    };

    return {
        register(thermostatComponent) {
            thermostatComponent.menuButton.button.addEventListener(
                'click', () => {
                    this.open();
                });
        },

        open() {
            if (baseElement) {
                // We already opened the menu! Allow the user to close it first
                return;
            }

            baseElement = document.createElement('div');
            baseElement.innerHTML = content;
            document.body.appendChild(baseElement);

            this.editScheduleButton =
                document.getElementById('menu-edit-sched');
            this.updateButton =
                document.getElementById('menu-update');

            setupMenuCancelButton(this);
            setupRefreshButton(this);
            setupOverlay(this);
            setupUpdateButton(this);
            checkForUpdates(this);

            this.timeout = setTimeout(
                () => this.close(), MENU_COMPONENT_TIMEOUT);
        },

        close() {
            if (!baseElement) {
                // We don't have a menu open!
                return;
            }
            baseElement.remove();
            baseElement = null;

            if (this.timeout) {
                clearTimeout(this.timeout);
                this.timeout = undefined;
            }
        },

    }
}

const menuComponent = createMenuComponent();
