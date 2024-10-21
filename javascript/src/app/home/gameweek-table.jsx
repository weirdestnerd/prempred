'use client'

import { useState, useMemo, useEffect } from 'react'
import { Subheading } from '@/components/heading'
import { Button } from '@/components/button'
import { getDummyGWGames } from '@/data'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'
import { Divider } from '@/components/divider'
import { Badge } from '@/components/badge'
import { debounce } from 'throttle-debounce';

import AcceptPredictionsModal from '@/app/home/ai/accept-predictions-modal'
import { API } from '@/api/base'

function PostGameWeekGame({ game }) {
    const homeTeamWin = game.scores.home_team > game.scores.away_team
    const awayTeamWin = game.scores.away_team > game.scores.home_team
    const draw = game.scores.home_team === game.scores.away_team
    const gotPrediction = useMemo(() => (game.user_prediction === game.home_team.short_name && homeTeamWin) ||
            (game.user_prediction === game.away_team.short_name && awayTeamWin) ||
            (game.user_prediction === 'draw' && draw), [game])

    function Team({ team, score, won }) {
        const bgColor = team.short_name === game.user_prediction ? `bg-${team.color}-900` : 'bg-white'
        const textColor = team.short_name === game.user_prediction ? 'text-white' : 'text-gray-900';

        return (
            <div key={team.short_name} className={`flex text-center rounded-lg ${bgColor} px-1 justify-center py-5 shadow`}>
                {won && <Badge className="rounded-full" color="cyan">w</Badge>}
                <dd className={`mt-1 ml-1 text-base ${ won ? 'underline underline-offset-8' : ''} tracking-tight ${textColor}`}>{score || 0}</dd>
                <dd className={`mt-1 ml-1 text-base font-semibold tracking-tight ${textColor}`}>{team.acronym.toUpperCase()}</dd>
            </div>
        )
    }

    return (
        <TableRow key={game.id} className="isolate rounded-md shadow-sm">
          <TableCell>
              <Team team={game.home_team} score={game.scores.home_team} won={homeTeamWin} />
          </TableCell>
          <TableCell>
              <Team team={game.away_team} score={game.scores.away_team} won={awayTeamWin} />
          </TableCell>
          <TableCell>
              {game.user_prediction && <Badge color={gotPrediction ? "lime" : "red"}>{gotPrediction ? '✅ +2' : '❌ -1'}</Badge>}
          </TableCell>
        </TableRow>
    )
}

function PreGameWeekGame({ game }) {
    const [prediction, setPrediction] = useState(game.user_prediction)
    const sendToApi = debounce(1000, () => {
        console.log("API CALL")
        fetch(API('predict-game'), { method: 'POST' })
    })

    const onPredictGame = (predict) => {
        if (prediction !== predict) sendToApi()
        setPrediction(predict)
    }

    function TeamButton({ team }) {

        return (
            <Button
                className="px-4 py-2"
                outline={prediction !== team.short_name}
                color={prediction === team.short_name ? team.color : ''}
                onClick={() => onPredictGame(team.short_name)}
              >
                {team.short_name}
              </Button>
        )
    }

    return (
        <TableRow key={game.id} className="isolate rounded-md shadow-sm">
          <TableCell>
              <TeamButton team={game.home_team} />
          </TableCell>
          <TableCell>
              <Button outline={prediction !== 'draw'} className="text-xs px-2 py-1" onClick={() => onPredictGame('draw')}>draw</Button>
          </TableCell>
          <TableCell>
              <TeamButton team={game.away_team} />
          </TableCell>
        </TableRow>
    )
}

function GameWeekGame({ game }) {
    let timeout;
    const [started, setStarted] = useState(new Date(game.started_at) <= new Date())

    useEffect(() => {
        const waitfor = new Date(game.started_at).getTime() - new Date().getTime()

        if (started) return;

        timeout = setTimeout(() => {
            setStarted(true)
        }, waitfor)

        return () => clearTimeout(timeout)
    }, [])

    return started ? <PostGameWeekGame game={game} /> : <PreGameWeekGame game={game} />
}

export function GameWeek({ gameweek }) {
    const { number, games } = gameweek

    const hasAIPred = games.some(g => !!g.ai_prediction)
    const gwStarted = new Date(games.sort((g1, g2) => new Date(g1.started_at).getTime() - new Date(g2.started_at).getTime())[0]?.started_at) <= new Date()

    const [predictionModalOpen, setPredictionModalOpen] = useState(false)

    // More gradients at: https://www.creative-tim.com/twcomponents/gradient-generator
    const classes = [
        hasAIPred ? "bg-gradient-to-r from-purple-500 to-pink-500 rounded px-6 py-6 " : null,
        gwStarted ? "bg-gradient-to-r from-indigo-400 to-cyan-400 rounded-md px-6 py-6 " : null,
        "mt-6"
    ]

    const dontShowModalAgainApi = () => {
        fetch(API('acknowledge-ai'), { method: 'POST' })
    }

    return (
        <div className={classes.join('')}>
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                  <h1 className={`text-base font-semibold leading-6 ${hasAIPred ? 'text-neutral-50' : 'text-gray-900'}`}>GW {number}</h1>
                  {hasAIPred ? <p className="mt-2 text-sm text-neutral-100">
                    Here's what our AI thinks you'll predict
                  </p> : <p className="mt-2 text-sm text-gray-700">
                    A look at your predictions for this game week
                  </p>}
                </div>
                <div className={`${hasAIPred && !gwStarted ? '' : 'hidden'} mt-4 sm:ml-16 sm:mt-0 sm:flex-none`}>
                  <button
                    type="button"
                    className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    onClick={() => setPredictionModalOpen(true)}
                  >
                    Accept
                  </button>
                </div>
            </div>
            <Divider className="my-4"/>
            <Table dense striped className="table-fixed mt-4 [--gutter:theme(spacing.3)] lg:[--gutter:theme(spacing.10)] ">
                <TableBody>
                  {games.map((game) => <GameWeekGame key={game.id} game={game} />)}
                </TableBody>
              </Table>
              <AcceptPredictionsModal open={predictionModalOpen} onClose={(dontShowAgain) => {
                  if (dontShowAgain) dontShowModalAgainApi();
                  setPredictionModalOpen(false)
              }}
              />
        </div>
    )
}