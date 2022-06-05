import React, { Component } from "react";
import { Event, SongSubmission } from "./models";

function parsedCookies(): {[key: string]: string} {
  const kvpairs = document.cookie.split(';');

  let out: {[key: string]: string} = {};

  kvpairs.forEach(s => {
    const ss = s.trim().split('=');
    if (ss.length == 2) {
      out[ss[0]] = ss[1];
    }
  });

  return out;
}

type SongTileProps = {
  sub?: SongSubmission,
}

class SongTile extends Component<SongTileProps, {}> {
  render() {
    const { sub } = this.props;

    if (sub === undefined) {
      return null;
    }

    const song = sub.song;
    const artist = song.artists[0];

    return (
      <div className="col-6">
        <h2>{song.title}</h2>
        <p>by {artist.name} on {artist.platform}</p>
      </div>
    );
  }
}

const questionIds = ["first_better", "first_peakier", "first_post_peakier"] as const;

type QuestionId = typeof questionIds[number];

type FormResponse = {
  [q in QuestionId]?: boolean;
}

type Props = {
  event: Event,
}

type State = {
  status: "ready" | "pending",
  message: string,
  sub1?: SongSubmission,
  sub2?: SongSubmission,
  response: FormResponse,
}

export default class RateSongs extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      status: "pending",
      message: "",
      response: {},
    };
  }

  componentDidMount() {
    this.newSong()
  }

  newSong() {
    this.setState({
      response: {},
    })

    fetch(`/api/pair?event=${this.props.event.id}`)
      .then(res => {
        res.json().then(data => {
          if (res.ok) {
            this.setState({
              sub1: data.result.sub1,
              sub2: data.result.sub2,
              status: "ready",
            })
          } else {
            this.setState({message: data.message, status: "ready"});
          }
        })
      })
      .catch(_ => this.setState({message: "An error occurred", status: "ready"}))

  }

  setFormValue(qid: QuestionId, value: boolean) {
    this.setState({
      response: {
        ...this.state.response,
        [qid]: value,
      }
    })
  }

  submit() {
    for (const qid of questionIds) {
      if (this.state.response[qid] === undefined) {
        this.setState({
          message: "Please answer all questions before submitting."
        });

        return;
      }
    }

    this.setState({
      status: "pending",
      message: "",
    })

    fetch("/api/song_comparisons", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': parsedCookies()['csrftoken'],
      },
      body: JSON.stringify({
        first_submission_id: this.state.sub1?.id,
        second_submission_id: this.state.sub2?.id,
        ...this.state.response,
      }),
    }).then(res => {
      if (res.ok) {
        this.newSong()
      } else {
        this.setState({
          message: "An error occurred",
          status: "ready",
        })
      }
    })
  }

  render() {
    const { sub1, sub2, status, message, response } = this.state;

    const content = () => {
      if (status === "pending") {
        return (
          <div className="center col-12">
            <img src="/static/img/spinner.gif" alt="Please wait a moment."/>
          </div>
        );
      } else {
        return (
          <>
            <SongTile sub={sub1}/>
            <SongTile sub={sub2}/>
          </>
        );
      }
    }

    const questionForm = (qid: QuestionId, text: string) => (
      <div className="col-12 col-md-6 rating-question">
        <h2>{text}</h2>

        <div>
          <div>{sub1?.song.title}</div>
          <div>{sub2?.song.title}</div>
        </div>

        <div>
          <div>
            <input type="radio" name={`${qid}_better`} value="true" checked={response[qid] === true}
                   onChange={e => this.setFormValue(qid, e.target.value === "true")}/>
          </div>
          <div>
            <input type="radio" name={`${qid}_better`} value="false" checked={response[qid] === false}
                   onChange={e => this.setFormValue(qid, e.target.value === "true")}/>
          </div>
        </div>
      </div>
    );

    return (
      <div className="row rate-songs">
        <div className="col-12">
          <h2>Please submit a rating for the below songs:</h2>
        </div>

        {content()}

        {questionForm("first_better", "Which song is better?")}
        {questionForm("first_peakier", "Which song is more energetic/danceable?")}
        {questionForm("first_post_peakier", "Which song is weirder?")}

        <div className="col-12 col-md-6">
          <div className="submit-button center">
            <h2 onClick={() => this.submit()}>Submit</h2>
          </div>
          <p>{message}</p>
        </div>
      </div>
    );
  }
}
