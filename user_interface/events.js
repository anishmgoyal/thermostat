const BaseSubscriptionNode = {
    children: null,
    parent: null,
    name: 'base',
    addChild(child) {
        this.children.push(child);
        child.parent = this;
    },
    dispatch(value) {
        for (let child of this.children) {
            child.dispatch(value);
        }
    },
    filter(predicate) {
        const node = createSubscriptionNode({
            dispatch(value) {
                if (predicate(value)) {
                    BaseSubscriptionNode.dispatch.call(node, value);
                }
            },
        });
        this.addChild(node);
        node.name = this.name + ' -> filter';
        return node;
    },
    map(mapper) {
        const node = createSubscriptionNode({
            dispatch(value) {
                BaseSubscriptionNode.dispatch.call(node, mapper(value));
            }
        });
        this.addChild(node);
        node.name = this.name + ' -> map';
        return node;
    },
    removeChild(child) {
        const idx = this.children.findIndex(it => it === child);
        if (idx > -1) {
            this.children.splice(idx, 1);
        }
    },
    subscribe(callback) {
        const node = createSubscriptionNode({
            dispatch(value) {
                callback(value);
                BaseSubscriptionNode.dispatch.call(node, value);
            },
        });
        this.addChild(node);
        return node;
    },
    unsubscribe() {
        if (this.parent) {
            this.parent.removeChild(this);
            this.parent = null;
        }
    },
};

function createSubscriptionNode(overrides = {}) {
    const node = Object.create(BaseSubscriptionNode, {
        children: {
            value: [],
        },
        parent: {
            value: null,
        },
    });

    Object.assign(node, overrides);
    return node;
}

function createSSEConnection() {
    const url = `${apiRoot}/events`;
    const baseSubscription = createSubscriptionNode({
        filter(filter) {
            const predicate = value => {
                const evType = value['event_type'];
                if (typeof filter === 'string') {
                    return filter === evType;
                } else if (Array.isArray(filter)) {
                    return filter.includes(evType);
                } else if (typeof filter === 'function') {
                    return filter(value);
                }
                console.warn(`Unsupported filter type ${filter} for base sub`);
                return false;
            };
            return BaseSubscriptionNode.filter.call(this, predicate);
        },
        onConfigUpdate(type) {
            const predicate = ({event_type, config_type}) =>
                event_type === 'update_configuration' && config_type === type;
            return BaseSubscriptionNode.filter.call(this, predicate);
        }
    });

    const sse = new EventSource(url);
    sse.addEventListener('message', ({data}) => {
        const message = JSON.parse(data);
        console.log('SSE Message', message);
        baseSubscription.dispatch(message);
    });
    return baseSubscription;
}

const sseSubscription = createSSEConnection();
