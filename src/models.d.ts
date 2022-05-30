/* This file has been autogenerated.
DO NOT manually edit it.
Run `python manage.py transpile_models` to update it. */

export type Artist = {
  id: number,
  name: string,
  platform: string,
  platform_id: string,
}

export type Song = {
  id: number,
  title: string,
  platform_id: string,
  artists: Artist[],
}

export type Event = {
  id: number,
  name: string,
  date: string,
  created_at: string,
}

export type SongSubmission = {
  id: number,
  event: Event,
  song: Song,
  created_at: string,
}

export type SongComparison = {
  id: number,
  first_submission: SongSubmission,
  second_submission: SongSubmission,
  created_at: string,
  first_better: boolean,
  first_peakier: boolean,
  first_post_peakier: boolean,
}
