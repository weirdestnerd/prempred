import { GameWeek } from '@/app/home/gameweek-table'
import { getDummyGW } from '@/data'

export const metadata = {
  title: 'Season',
}

async function getSeason() {
    const res = await fetch('http://localhost:5000/season')
    return res.json()
}

export default async function Season() {
    const season = await getSeason();
    return season.map(gw => <GameWeek key={gw.number} gameweek={gw} />)
}
