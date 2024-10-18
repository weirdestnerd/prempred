import { getEvents } from '@/data'
import '@/styles/tailwind.css'

import { ApplicationLayout } from './application-layout'

export const metadata = {
  title: {
    template: '%s - PremPred',
    default: 'PremPred',
  },
  description: 'Make your Premier League predictions',
}

export default async function RootLayout({ children }) {
  let events = await getEvents()

  return (
    <html
      lang="en"
      className="text-zinc-950 antialiased lg:bg-zinc-100 dark:bg-zinc-900 dark:text-white dark:lg:bg-zinc-950"
    >
      <head>
        <link rel="preconnect" href="https://rsms.me/" />
        <link rel="stylesheet" href="https://rsms.me/inter/inter.css" />
      </head>
      <body>
        <ApplicationLayout events={events}>{children}</ApplicationLayout>
        <footer className="">
          <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
            <div className="flex justify-center space-x-6 md:order-2">
            </div>
            <div className="md:order-1 md:mt-0">
              <p className="text-center text-xs leading-5 text-gray-500">
                Made with ❤️ by <a href="https://linkedin.com/in/oludavid" target="_blank">Olu</a>
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}
