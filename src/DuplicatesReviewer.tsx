import React, { Component } from "react";
import { Event, DuplicationFlag } from "./models";
import ResourceManager from "./ResourceManager";
import SongPairTile from "./SongPairTile";

type Props = {
  event: Event,
}

type State = {
  unreviewed_flags: DuplicationFlag[],
}

export default class DuplicatesReviewer extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      unreviewed_flags: [],
    };
  }

  componentDidMount() {
    ResourceManager.getModels('unreviewed_duplication_flags')
      .then(unreviewed_flags => this.setState({unreviewed_flags}));
  }


  render() {
    return (
      <div className="duplicates-reviewer">
        {this.state.unreviewed_flags.map(flag => (
          <>
            <h2>Are these songs duplicates?</h2>
            <SongPairTile sub1={flag.existing_submission} sub2={flag.new_submission}/>
          </>
        ))}
      </div>
    );
  }
}
