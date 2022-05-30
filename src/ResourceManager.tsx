import { Event } from "./models";

type fetchable_models = {
  events: Event,
}

type ResourceManagerState = {
  [K in keyof fetchable_models]?: fetchable_models[K][]
}

class _ResourceManager {
  state: ResourceManagerState;

  constructor() {
    this.state = {};
  }

  getModels<K extends keyof fetchable_models>(k: K): Promise<fetchable_models[K][]> {
    const current_list = this.state[k]

    if (current_list === undefined) {
      return fetch(`/api/${k}`)
        .then(response => response.json())
        .then(data => {
          this.state[k] = data.results;
          return data.results;
        })
    } else {
      return Promise.resolve(current_list as fetchable_models[K][]);
    }
  }
}

const ResourceManager = new _ResourceManager();
export default ResourceManager;
