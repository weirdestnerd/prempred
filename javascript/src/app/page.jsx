import { Avatar } from '@/components/avatar'
import { Badge } from '@/components/badge'
import { Divider } from '@/components/divider'
import { Heading, Subheading } from '@/components/heading'
import { Select } from '@/components/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'
import { getRecentOrders, getDummyGWGames, getDummyGW } from '@/data'
import { GameWeek } from '@/app/home/gameweek-table'
import { API_URL } from '@/api/base'

function getTimeBasedGreeting() {
  const now = new Date();
  const hour = now.getHours();

  if (hour < 12) {
    return "Good morning";
  } else if (hour < 18) {
    return "Good afternoon";
  } else {
    return "Good evening";
  }
}

async function getCurrentGameWeek() {
  const res = await fetch(`${API_URL}/current-gw`, { cache: 'no-store'})
  return res.json()
}

async function getLeaderboard() {
    const res = await fetch(`${API_URL}/leaderboard`)
    return res.json()
}

export default async function Home() {
    const gameweek = await getCurrentGameWeek()
    const leaderboard = await getLeaderboard()

  return (
    <>
      <Heading>{getTimeBasedGreeting()}</Heading>

      <GameWeek gameweek={gameweek} />

      <Subheading className="mt-14">Leaderboard</Subheading>

      <Table className="mt-4 [--gutter:theme(spacing.6)] lg:[--gutter:theme(spacing.10)]">
        <TableHead>
          <TableRow>
            <TableHeader>#</TableHeader>
            <TableHeader>User</TableHeader>
            <TableHeader>GW 1</TableHeader>
            <TableHeader className="text-right">Total</TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {leaderboard.map((info, index) => (
            <TableRow key={info.user_name}>
              <TableCell>{index + 1}</TableCell>
              <TableCell>{info.user_name}</TableCell>
              <TableCell className="text-zinc-500">{info.current_game_week_points}</TableCell>

              <TableCell className="text-right">{info.total_points}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  )
}
