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
  subs: SongSubmission[],
}

export default class SongsTile extends Component<Props, {}> {
  render() {
    const { subs } = this.props;

    const outerStyle = {display: "flex", justifyContent: "space-around"};
    const style = {flex: 1};

    return (
      <div className="col-12">
        <div style={outerStyle}>
          {subs.map((sub, i) => (
            <h2 style={style} key={i}>{sub.song.title}</h2>
          ))}
        </div>

        <div style={outerStyle}>
          {subs.map((sub, i) => (
            <p style={style} key={i}>{byline(sub.song)}</p>
          ))}
        </div>

        <div style={outerStyle}>
          {subs.map((sub, i) => (
            <div style={{...style, padding: "1vw"}} key={i}>{Embed(sub.song)}</div>
          ))}
        </div>
      </div>
    );
  }
}