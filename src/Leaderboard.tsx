import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSort, faSortUp, faSortDown } from "@fortawesome/free-solid-svg-icons";

import {User, Event, SongComparison} from "./models";
import ResourceManager, {ScoreSuite} from "./ResourceManager";

function round(n: number, digits: number) {
  const pow10 = Math.pow(10, digits);
  return Math.round(n*pow10) / pow10;
}

type LeaderboardProps<T> = {
  items: T[],
  columns: [string, keyof T][],
}

type LeaderboardState<T> = {
  sort_key: keyof T,
  ascending: boolean,
}

class Leaderboard<T> extends Component<LeaderboardProps<T>, LeaderboardState<T>>{
  constructor(props: LeaderboardProps<T>) {
    super(props);
    this.state = {
      sort_key: props.columns[0][1],
      ascending: false,
    }
  }

  setColumn(col: keyof T) {
    if (this.state.sort_key === col) {
      this.setState({
        ascending: !this.state.ascending,
      })
    } else {
      this.setState({
        sort_key: col,
        ascending: false,
      })
    }
  }

  sortIcon(col: keyof T) {
    if (col !== this.state.sort_key) {
      return faSort;
    } else if (this.state.ascending) {
      return faSortUp;
    } else {
      return faSortDown;
    }
  }

  render() {
    const { sort_key, ascending } = this.state;

    const sortedItems = this.props.items.sort((i1, i2) => {
      let out = i1[sort_key] < i2[sort_key] ? -1 : 1;

      return ascending ? out : -out;
    })

    return (
      <div className="row leaderboard">
        <div className="leaderboard-row col-12">
          {this.props.columns.map((col, i) => (
            <div className="leaderboard-td" key={i}>
              <a href="#" onClick={() => this.setColumn(col[1])}>
                {col[0]}
                {' '}
                <FontAwesomeIcon icon={this.sortIcon(col[1])}/>
              </a>
            </div>
          ))}
        </div>

        {sortedItems.map((item, i) => (
          <div className="leaderboard-row col-12" key={i}>
            {this.props.columns.map((col, j) => (
              <div className="leaderboard-td" key={j}>
                {item[col[1]]}
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  }
}

type UserTableRow = {
  name: string,
  email: string,
  submissions: number,
  votes: number,
}

function instantiateUserRow(u: User): UserTableRow {
  return {
    name: `${u.first_name} ${u.last_name}`,
    email: u.email,
    submissions: 0,
    votes: 0,
  }
}

type SongTableRow = {
  title: string,
  artists: string,
  platform: string,
  quality_score: number,
  energy_score: number,
  post_peak_score: number,
  info_score: number,
}

type Props = {
  event: Event,
}

type State = {
  comparisons?: SongComparison[],
  score_suites?: ScoreSuite[],
}

export default class LeaderboardPage extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    const event_id = `${this.props.event.id}`;

    ResourceManager.getModels('song_comparisons', {event: event_id})
      .then(comparisons => this.setState({comparisons}))

    ResourceManager.getModels('score_suites', {event: event_id})
      .then(score_suites => this.setState({score_suites}));
  }

  computeUserTableValues(): UserTableRow[] {
    let rowsById: {[key: number]: UserTableRow} = {};

    this.state.score_suites?.forEach(s => {
      const u = s.song_submission.submitter;
      rowsById[u.id] = rowsById[u.id] || instantiateUserRow(u);
      rowsById[u.id].submissions += 1;
    })

    this.state.comparisons?.forEach(c => {
      rowsById[c.voter.id] = rowsById[c.voter.id] || instantiateUserRow(c.voter);
      rowsById[c.voter.id].votes += 1;
    });

    return Object.values(rowsById);
  }

  computeSubmissionTableValues(): SongTableRow[] {
    return (this.state.score_suites || []).map(s => ({
      title: s.song_submission.song.title,
      artists: s.song_submission.song.artists.map(a => a.name).join(', '),
      platform: s.song_submission.song.artists[0].platform,
      quality_score: round(s.quality_score, 1),
      energy_score: round(s.energy_score, 1),
      post_peak_score: round(s.post_peak_score, 1),
      info_score: s.info_score,
    }))
  }

  render() {
    const { score_suites, comparisons } = this.state;

    if (score_suites === undefined || comparisons === undefined) {
      return (
        <div className="row">
          <div className="center col-12">
            <img src="/static/img/spinner.gif" alt="Please wait a moment."/>
          </div>
        </div>
      );
    }

    const ratio = 2*comparisons.length/score_suites.length;

    return (
      <>
        <div className="row">
          <div className="col-12">
            <p>
              There have been {score_suites.length} songs submitted
              and {comparisons.length} votes submitted. The average
              song has {round(ratio, 2)} votes. The voting
              process is {Math.round(ratio * 8)}% finished.
            </p>
          </div>
        </div>
        <Leaderboard items={this.computeUserTableValues()} columns={[
          ['Name', 'name'],
          ['Email address', 'email'],
          ['Songs submitted', 'submissions'],
          ['Votes submitted', 'votes'],
        ]}/>
        <Leaderboard items={this.computeSubmissionTableValues()} columns={[
          ['Title', 'title'],
          ['Artists', 'artists'],
          ['Platform', 'platform'],
          ['Quality Score', 'quality_score'],
          ['Energy Score', 'energy_score'],
          ['Post-peak score', 'post_peak_score'],
          ['Votes', 'info_score'],
        ]}/>
      </>
    );
  }
}
