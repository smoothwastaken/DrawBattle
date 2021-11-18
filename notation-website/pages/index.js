import React, { useState, useEffect } from "react";
import Head from "next/head";
import Header from "../components/Header";
import ResultComponent from "../components/ResultComponent";

import toast, { Toaster } from "react-hot-toast";
import { motion, AnimatePresence } from "framer-motion";

const config = require("../dbconfig.json");
const users = config.users;

const timeToVote = config.timeToVote;

export default function Home() {
  const [seconds, setSeconds] = useState(timeToVote);
  const [userInt, setUserInt] = useState(0);
  const [end, setEnd] = useState(0);
  const [selected, setSelected] = useState("0");

  if (seconds === -1) {
    setUserInt((userInt) => userInt + 1);
    setSeconds(timeToVote);
    setSelected("0");
    if (users.length <= userInt + 1) {
      setEnd(1);
      console.log("There is no more players.");
    } else {
      toast.success("Joueur suivant!");
      console.log(`Next player (${users[userInt]}).`);
    }
  }

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((seconds) => seconds - 1);
    }, 1000);
  }, []);

  return (
    <AnimatePresence>
      <div className="bg-white h-screen">
        <Toaster />
        <Head>
          <title>DrawBattle - Results</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <main>
          <Header time={timeToVote} end={end} />
          <div className="m-10">
            <ResultComponent
              username={users[userInt]}
              selected={selected}
              setSelected={setSelected}
            />
            {end === 1 ? (
              <>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex justify-center z-50 select-none items-center absolute blur-xl top-0 left-0 w-screen h-screen bg-black bg-opacity-60"
                >
                  <motion.div
                    initial={{ y: -100 }}
                    animate={{ y: 0 }}
                    className="m-20 p-14 select-none bg-white rounded-2xl text-center cursor-default"
                  >
                    <h1 className="text-4xl font-title font-semibold mb-2">
                      Les votes sont clos !
                    </h1>
                    <p className="font-body">
                      Toutes les créations de chaque joueur ont reçu une note de
                      chacun.
                      <br />
                      Voyons voir qui a gagné cette partie !
                      <br />
                      Pour connaître le résultat, il te suffit de regarder sur
                      le script Python :)
                      <br />
                      Alors, qui a gagné ?
                    </p>
                  </motion.div>
                </motion.div>
              </>
            ) : (
              <></>
            )}
          </div>
        </main>
      </div>
    </AnimatePresence>
  );
}
