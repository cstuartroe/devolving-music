import React, { Component } from "react";
import { safePost } from "./utils";
import {Event, SongSubmission} from "./models";
import SongPairTile from "./SongPairTile";


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
  color1?: string,
  color2?: string,
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
              ...data.results,
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

    safePost("/api/song_comparisons", {
      first_submission_id: this.state.sub1?.id,
      second_submission_id: this.state.sub2?.id,
      ...this.state.response,
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
    const { sub1, sub2, color1, color2, status, message, response } = this.state;

    const content = () => {
      if (status === "pending") {
        return (
          <div className="center col-12">
            <img src="/static/img/spinner.gif" alt="Please wait a moment."/>
          </div>
        );
      } else {
        return <SongPairTile sub1={sub1} sub2={sub2}/>;
      }
    }

    const rad = 15;

    const questionButton = (qid: QuestionId, formValue: boolean, sub?: SongSubmission, color?: string) => (
      <div
        className="col-6 rating-question-option center"
        onClick={() => this.setFormValue(qid, formValue)}
        style={{
          backgroundColor: (response[qid] === formValue) ? `#${color}` : '#333333',
          borderRadius: formValue ? `${rad}px 0 0 ${rad}px` : `0 ${rad}px ${rad}px 0`,
        }}
      >
        <div>{sub?.song.title}</div>
      </div>
    );

    const questionForm = (qid: QuestionId, text: string) => (
      <div className="row rating-question">
        <div className="col-12 rating-question-text">
          <h2>{text}</h2>
        </div>

        {questionButton(qid, true, sub1, color1)}
        {questionButton(qid, false, sub2, color2)}
      </div>
    );

    return (
      <div className="rate-songs">
        <div className="row">
          {content()}
        </div>

        {questionForm("first_better", "Which song is better?")}
        {questionForm("first_peakier", "Which song is more energetic/danceable?")}
        {questionForm("first_post_peakier", "Which song is weirder?")}

        <div className="col-12">
          <div className="submit-button center">
            <h2 onClick={() => this.submit()}>Submit</h2>
          </div>
          <p>{message}</p>
        </div>
      </div>
    );
  }
}
