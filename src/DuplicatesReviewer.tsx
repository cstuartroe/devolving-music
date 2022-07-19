import React, { Component } from "react";
import { Event, DuplicationFlag, DuplicationFlag_status } from "./models";
import ResourceManager from "./ResourceManager";
import SongsTile from "./SongsTile";
import { safePost } from "./utils";

type VoterProps = {
  flag_id: number,
}

type VoterState = {
  status: DuplicationFlag["status"],
  message: string,
}

class DuplicatesVoter extends Component<VoterProps, VoterState> {
  constructor(props: VoterProps) {
    super(props);

    this.state = {
      status: "unreviewed",
      message: "",
    };
  }

  sendVote(status: DuplicationFlag["status"]) {
    if (status === this.state.status) { return; }

    const original_status = this.state.status;

    this.setState({status, message: ""});

    const onError = () => {
      this.setState({
        status: original_status,
        message: "An error occurred.",
      });
    }

    safePost("/api/unreviewed_duplication_flags", {
      id: this.props.flag_id,
      status,
    }).then(res => {
      if (!res.ok) {
        onError();
      }
    }).catch(_ => onError());
  }

  render() {
    const choiceTile = (status: DuplicationFlag["status"], text: string, borderRadius: string) => {
      return (
        <div
          className={`col-4 center button ${(this.state.status === status ? "selected" : "")}`}
          style={{borderRadius: borderRadius}}
          onClick={() => this.sendVote(status)}>

          <p style={{marginBottom: 0}}>{text}</p>
        </div>
      );
    }

    return (
      <>
        {choiceTile("unrelated", "Unrelated", "10px 0 0 10px")}
        {choiceTile("different_versions", "Different versions", "0")}
        {choiceTile("duplicate", "The same", "0 10px 10px 0")}
        <div className="col-12"><p>{this.state.message}</p></div>
      </>
    );
  }
}

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
          <div className="row" key={flag.id}>
            <div className="col-12">
              <h2>Are these songs duplicates?</h2>
            </div>
            <SongsTile subs={[flag.existing_submission, flag.new_submission]}/>
            <DuplicatesVoter flag_id={flag.id}/>
          </div>
        ))}
        {this.state.unreviewed_flags.length === 0 && (
          <div className="row">
            <div className="col-12">
              <p>No duplicates to review!</p>
            </div>
          </div>
        )}
      </div>
    );
  }
}
