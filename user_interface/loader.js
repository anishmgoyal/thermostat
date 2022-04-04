function createLoader() {
    let isLoading = false;
    const queue = [];
    const loadedScripts = new Set();

    function checkQueue() {
        if (isLoading) {
            return;
        }

        if (queue.length) {
            const script = queue.shift();
            doScriptLoad(script);
        }
    }

    function doScriptLoad(script) {
        if (isLoading) {
            return;
        }

        console.debug(`Start loading ${script}`);
        isLoading = true;

        const scriptElem = document.createElement('script');
        scriptElem.type = 'text/javascript';
        scriptElem.src = script;
        scriptElem.addEventListener('load', () => {
            console.debug(`Successfully loaded ${script}`);
            finishScriptLoad();
        });
        scriptElem.addEventListener('error', err => {
            console.error(`Failed to load script ${script}`, err);
            finishScriptLoad();
        });
        document.body.append(scriptElem);
    }

    function finishScriptLoad() {
        isLoading = false;
        checkQueue();
    }

    return {
        loadScript(script) {
            if (loadedScripts.has(script)) {
                console.debug(`Skipping duplicate load of script ${script}`);
                return;
            }
            loadedScripts.add(script);

            console.debug(`Enqueueing ${script} for load`);
            queue.push(`${script}?t=${new Date().getTime()}`);
            checkQueue();
        },
    };
}

const scriptLoader = createLoader();
