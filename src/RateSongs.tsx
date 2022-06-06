import React, { Component } from "react";
import { safePost } from "./utils";
import {Event, Song, SongSubmission} from "./models";

const embedHeight = "150";

function SpotifyEmbed(platform_id: string) {
  return (
    <iframe
      style={{borderRadius: "12px"}} id={`embed-${platform_id}`}
      src={`https://open.spotify.com/embed/track/${platform_id}?utm_source=generator`}
      width="100%" height={embedHeight} frameBorder="0" allowFullScreen
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"/>
  );
}

function YouTubeEmbed(platform_id: string) {
  return (
    <iframe
      id={`embed-${platform_id}`} title="YouTube video player"
      src={`https://www.youtube.com/embed/${platform_id}`}
      width="100%" height={embedHeight} frameBorder="0" allowFullScreen
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"/>
  );
}

function Embed(song: Song) {
  console.log(song);

  switch (song.artists[0].platform) {
    case "Spotify":
      return SpotifyEmbed(song.platform_id);
    case "YouTube":
      return YouTubeEmbed(song.platform_id);
    case "Soundcloud":
      return <div/>
  }
}

function byline(song: Song) {
  const artist = song.artists[0];

  return `by ${artist.name} on ${artist.platform}`
}

type SongTileProps = {
  sub1?: SongSubmission,
  sub2?: SongSubmission,
}

class SongTile extends Component<SongTileProps, {}> {
  render() {
    const { sub1, sub2 } = this.props;

    if (sub1 === undefined || sub2 === undefined) {
      return null;
    }

    const outerStyle = {display: "flex", justifyContent: "space-around"};
    const style = {flex: 1};

    return (
      <div className="col-12">
        <div style={outerStyle}>
          <h2 style={style}>{sub1.song.title}</h2>
          <h2 style={style}>{sub2.song.title}</h2>
        </div>

        <div style={outerStyle}>
          <p style={style}>{byline(sub1.song)}</p>
          <p style={style}>{byline(sub2.song)}</p>
        </div>

        <div style={outerStyle}>
          <div style={{...style, padding: "1vw"}}>{Embed(sub1.song)}</div>
          <div style={{...style, padding: "1vw"}}>{Embed(sub2.song)}</div>
        </div>
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
              ...data.result,
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
        return <SongTile sub1={sub1} sub2={sub2}/>;
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
