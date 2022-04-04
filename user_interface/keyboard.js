function createKeyboardComponent() {
  const MAX_LEN = 25;

  /** @type {HTMLElement} */
  let baseElement = null;
  let content = `
    <div class="keyboard" id="keyboard-overlay">
      <div class="keyboard-wrapper">
        <div class="keyboard-exit-control">
          <button class="cancel-button">
            <i class="fa-solid fa-circle-xmark"></i>
          </button>
        </div>
        <div class="keyboard-display-row">
          <div class="keyboard-display"></div>
          <div class="keyboard-display-cursor">
            <i class="fa-solid fa-i-cursor"></i>
          </div>
        </div>
        <div class="keyboard-buttons">
          <div class="keyboard-row">
            <button class="keyboard-button keyboard-button-number">1</button>
            <button class="keyboard-button keyboard-button-number">2</button>
            <button class="keyboard-button keyboard-button-number">3</button>
            <button class="keyboard-button keyboard-button-number">4</button>
            <button class="keyboard-button keyboard-button-number">5</button>
            <button class="keyboard-button keyboard-button-number">6</button>
            <button class="keyboard-button keyboard-button-number">7</button>
            <button class="keyboard-button keyboard-button-number">8</button>
            <button class="keyboard-button keyboard-button-number">9</button>
            <button class="keyboard-button keyboard-button-number">0</button>
          </div>
          <div class="keyboard-row">
            <button class="keyboard-button keyboard-button-letter">q</button>
            <button class="keyboard-button keyboard-button-letter">w</button>
            <button class="keyboard-button keyboard-button-letter">e</button>
            <button class="keyboard-button keyboard-button-letter">r</button>
            <button class="keyboard-button keyboard-button-letter">t</button>
            <button class="keyboard-button keyboard-button-letter">y</button>
            <button class="keyboard-button keyboard-button-letter">u</button>
            <button class="keyboard-button keyboard-button-letter">i</button>
            <button class="keyboard-button keyboard-button-letter">o</button>
            <button class="keyboard-button keyboard-button-letter">p</button>
          </div>
          <div class="keyboard-row">
            <button class="keyboard-button keyboard-button-letter">a</button>
            <button class="keyboard-button keyboard-button-letter">s</button>
            <button class="keyboard-button keyboard-button-letter">d</button>
            <button class="keyboard-button keyboard-button-letter">f</button>
            <button class="keyboard-button keyboard-button-letter">g</button>
            <button class="keyboard-button keyboard-button-letter">h</button>
            <button class="keyboard-button keyboard-button-letter">j</button>
            <button class="keyboard-button keyboard-button-letter">k</button>
            <button class="keyboard-button keyboard-button-letter">l</button>
          </div>
          <div class="keyboard-row">
            <button class="keyboard-button keyboard-button-special caps-up-button">
              <i class="fa-solid fa-circle-up"></i>
            </button>
            <button class="keyboard-button keyboard-button-special caps-down-button">
              <i class="fa-solid fa-circle-down"></i>
            </button>
            <button class="keyboard-button keyboard-button-letter">z</button>
            <button class="keyboard-button keyboard-button-letter">x</button>
            <button class="keyboard-button keyboard-button-letter">c</button>
            <button class="keyboard-button keyboard-button-letter">v</button>
            <button class="keyboard-button keyboard-button-letter">b</button>
            <button class="keyboard-button keyboard-button-letter">n</button>
            <button class="keyboard-button keyboard-button-letter">m</button>
            <button class="keyboard-button keyboard-button-special del-button">
              <i class="fa-solid fa-delete-left"></i>
            </button>
          </div>
          <div class="keyboard-row">
            <button class="keyboard-button keyboard-button-special cancel-button">
              cancel
            </button>
            <button class="keyboard-button keyboard-button-space space-button">
              space
            </button>
            <button class="keyboard-button keyboard-button-special done-button">
              done
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  /** @type {HTMLElement} */
  let displayComponent;
  /** @type {HTMLElement} */
  let capsUpButton;
  /** @type {HTMLElement} */
  let capsDownButton;
  let capsLock = false;

  /** @type {(string) => void} */
  let resolve;
  /** @type {(Error) => void} */
  let reject;

  function appendToText(value) {
    if (displayComponent.innerText.length >= MAX_LEN) {
      return;
    }
    displayComponent.innerHTML += value;
  }

  function deleteFromText() {
    if (displayComponent.innerText.length) {
      displayComponent.innerText = displayComponent.innerText.substring(
        0, displayComponent.innerText.length - 1);
    }
  }

  function setupNumberKeys() {
    const numKeys =
      baseElement.getElementsByClassName('keyboard-button-number');
    for (let numKey of numKeys) {
      numKey.addEventListener('click', (event) => {
        appendToText(event.target.innerText);
      });
    }
  }

  function setupLetterKeys() {
    const letterKeys =
      baseElement.getElementsByClassName('keyboard-button-letter');
    for (let letterKey of letterKeys) {
      letterKey.addEventListener('click', (event) => {
        appendToText(event.target.innerText);
      });
    }
  }

  function switchCase(isCaps) {
    const letterKeys =
      baseElement.getElementsByClassName('keyboard-button-letter');
    for (let letterKey of letterKeys) {
      if (isCaps) {
        letterKey.innerText = letterKey.innerText.toUpperCase();
      } else {
        letterKey.innerText = letterKey.innerText.toLowerCase();
      }
    }
  }

  function setupCapsLock() {
    const capsUpButton =
      baseElement.getElementsByClassName('caps-up-button')[0];
    const capsDownButton =
      baseElement.getElementsByClassName('caps-down-button')[0];

    capsUpButton.addEventListener('click', () => {
      capsUpButton.style.display = 'none';
      capsDownButton.style.display = '';
      switchCase(true);
    });

    capsDownButton.addEventListener('click', () => {
      capsUpButton.style.display = '';
      capsDownButton.style.display = 'none';
      switchCase(false);
    });

    capsUpButton.style.display = '';
    capsDownButton.style.display = 'none';
  }

  function setupDelKey() {
    const delKey =
      baseElement.getElementsByClassName('del-button')[0];
    delKey.addEventListener('click', deleteFromText);
  }

  function setupCancelKey() {
    const cancelKeys =
      baseElement.getElementsByClassName('cancel-button');
    for (let cancelKey of cancelKeys) {
      cancelKey.addEventListener('click', () => {
        baseElement.remove();
        reject(new Error('User cancelled entry'));
      });
    }
  }

  function setupSpaceKey() {
    const spaceKey =
      baseElement.getElementsByClassName('space-button')[0];
    spaceKey.addEventListener('click', () => {
      appendToText('&nbsp;');
    });
  }

  function setupDoneKey() {
    const doneKey =
      baseElement.getElementsByClassName('done-button')[0];
    doneKey.addEventListener('click', () => {
      if (displayComponent.innerText.length) {
        baseElement.remove();
        resolve(displayComponent.innerText);
      }
    });
  }

  return {
    /** @type {(startingText: string) => Promise<string>} */
    openKeyboard(startingText = '') {
      if (!baseElement) {
        baseElement = document.createElement('div');
        baseElement.innerHTML = content;

        displayComponent =
          baseElement.getElementsByClassName('keyboard-display')[0];
        
        setupNumberKeys();
        setupLetterKeys();
        setupDelKey();
        setupCancelKey();
        setupSpaceKey();
        setupDoneKey();
      }

      // This needs to be set up every time, to reset state
      setupCapsLock();
      displayComponent.innerText = startingText;
      document.body.appendChild(baseElement);
      console.log('opening keyboard');
      return new Promise((_resolve, _reject) => {
        resolve = _resolve;
        reject = _reject;
      });
    }
  }
}

const keyboardComponent = createKeyboardComponent();
