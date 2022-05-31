import React, { Component } from "react";
import { Event, Artist_platform } from "./models";

type Props = {
  platform: typeof Artist_platform[number],
  event: Event,
}

type State = {
  link: string,
  status: "unsubmitted" | "pending" | "submitted",
  message: string,
}

export default class SubmitPlaylist extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      link: "",
      status: "unsubmitted",
      message: " ",
    }
  }

  presubmit(): boolean {
    if (this.state.link.length === 0) {
      this.setState({
        message: "Can't be empty.",
      })

      return false;
    }

    return true;
  }

  submit() {
    if (!this.presubmit()) {
      return;
    }

    this.setState({
      status: "pending",
      message: "",
    })

    fetch(`/api/submit-playlist/${this.props.platform}`, {
      method: "POST",
      body: JSON.stringify({
        event: this.props.event.id,
        playlist_link: this.state.link,
      })
    }).then(response => {
      if (response.ok) {
        this.setState({
          status: "submitted",
          message: "The playlist was submitted!"
        })
      } else {
        response.json().then(data => {
          this.setState({
            status: "unsubmitted",
            message: data.message,
          })
        })
      }
    }).catch(_ => this.setState({
      status: "unsubmitted",
      message: "An unexpected error occurred."
    }))
  }

  render() {
    const { platform } = this.props;

    const bottomElement = () => {
      if (this.state.status === "pending") {
        return <img src="/static/img/spinner.gif" alt="Please wait a moment."/>;
      } else {
        return <h2 onClick={() => this.submit()}>Submit</h2>;
      }
    }

    const content = () => {
      if (this.state.status === "submitted") {
        return (
          <div className="col-12">
            <p>{this.state.message}</p>
          </div>
        );
      } else {
        return <>
          <div className="col-12" style={{paddingBottom: "2vh"}}>
            <h2>Please submit a link to a {platform} playlist below:</h2>
          </div>

          <div className="col-2"/>

          <div className="col-8">
            <input type="text" onChange={e => this.setState({link: e.target.value})}/>

            <p style={{color: "red"}}>{this.state.message}</p>

            <div className="playlist-submit-button">
              {bottomElement()}
            </div>
          </div>
        </>;
      }
    }

    return (
      <div className="row submit-playlist">
        {content()}
      </div>
    );
  }
}
