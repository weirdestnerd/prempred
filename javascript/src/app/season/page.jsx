import { GameWeek } from '@/app/home/gameweek-table'
import { getDummyGW } from '@/data'
import { API } from '@/api/base'

export const metadata = {
  title: 'Season',
}

async function getSeason() {
    const res = await fetch(API('season'))
    return res.json()
}

export default async function Season() {
    const season = await getSeason();
    return season.map(gw => <GameWeek key={gw.number} gameweek={gw} />)
}
