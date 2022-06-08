import React, {Component} from "react";
import {Song, SongSubmission} from "./models";

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

type Props = {
  sub1?: SongSubmission,
  sub2?: SongSubmission,
}

export default class SongPairTile extends Component<Props, {}> {
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