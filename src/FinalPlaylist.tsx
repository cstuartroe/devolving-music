import React, { Component } from "react";

import { Event, SongSubmission } from "./models";
import SongsTile from "./SongsTile";

type SongScore = {
  song_submission: SongSubmission,
  energy_score: number,
  quality_score: number,
  post_peak_score: number,
}

type Props = {
  event: Event
};

type State = {
  song_scores: SongScore[],
}

export default class FinalPlaylist extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      song_scores: [],
    }
  }

  componentDidMount() {
    fetch(`/api/final_playlist?event=${this.props.event.id}`)
      .then(res => res.json())
      .then(data => this.setState({
        song_scores: data.results,
      }))
  }

  render() {
    return (
      <div className="row final-playlist">
        {this.state.song_scores.map((score, i) => (
          <SongsTile subs={[score.song_submission]} key={i}/>
        ))}
      </div>
    );
  }
}
