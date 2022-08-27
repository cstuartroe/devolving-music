import React, { Component } from "react";

import { Event } from "./models";
import SongsTile from "./SongsTile";
import {ScoreSuite} from "./ResourceManager";

type Props = {
  event: Event
};

type State = {
  song_scores: ScoreSuite[],
}

export default class CurrentPlaylist extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      song_scores: [],
    }
  }

  componentDidMount() {
    fetch(`/api/current_playlist?event=${this.props.event.id}`)
      .then(res => res.json())
      .then(data => this.setState({
        song_scores: data.results,
      }))
  }

  render() {
    return (
      <div className="row current-playlist">
        {this.state.song_scores.map((score, i) => (
          <SongsTile subs={[score.song_submission]} key={i}/>
        ))}
      </div>
    );
  }
}
