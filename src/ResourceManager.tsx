import {Event, DuplicationFlag, SongSubmission, SongComparison} from "./models";

export type ScoreSuite = {
  song_submission: SongSubmission,
  energy_score: number,
  quality_score: number,
  post_peak_score: number,
  info_score: number,
}

type fetchable_models = {
  events: [Event, {}],
  unreviewed_duplication_flags: [DuplicationFlag, {}],
  score_suites: [ScoreSuite, {event: string}],
  song_comparisons: [SongComparison, {event: string}],
}

type ResourceManagerState = {
  [K in keyof fetchable_models]?: fetchable_models[K][0][]
}

class _ResourceManager {
  state: ResourceManagerState;

  constructor() {
    this.state = {};
  }

  getModels<K extends keyof fetchable_models>(k: K, params?: fetchable_models[K][1]): Promise<fetchable_models[K][0][]> {
    const current_list = this.state[k]

    if (current_list === undefined) {
      let uri = `/api/${k}`;

      if (params !== undefined) {
        uri = uri + '?' + new URLSearchParams(params);
      }

      return fetch(uri)
        .then(response => response.json())
        .then(data => {
          this.state[k] = data.results;
          return data.results;
        })
    } else {
      return Promise.resolve(current_list as fetchable_models[K][0][]);
    }
  }
}

const ResourceManager = new _ResourceManager();
export default ResourceManager;
