import React, { useState } from "react";
import Image from "next/image";

import toast, { Toaster } from "react-hot-toast";
import { motion } from "framer-motion";

import { StarIcon } from "@heroicons/react/outline";

import VoteButtons from "./VoteButtons";

const config = require("../dbconfig.json");
const theme = config.theme;

const ResultComponent = ({ username, selected, setSelected }) => {
  const containerVariant = {
    hidden: {
      x: 100,
      opacity: 0,
    },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        delay: 0.5,
        type: "spring",
        bounce: 0,
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const item = {
    hidden: {
      x: 50,
      opacity: 0,
    },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        type: "spring",
        bounce: 0,
      },
    },
  };

  return (
    <motion.div
      variants={containerVariant}
      initial="hidden"
      animate="visible"
      className="flex gap-6 font-body"
    >
      <motion.div
        variants={item}
        className="shadow-2xl select-none border-2 border-gray-500 cursor-help z-40"
        drag
        dragConstraints={{
          right: 0,
          left: 0,
          top: 0,
          bottom: 0,
        }}
        whileDrag={{
          borderRadius: 50,
        }}
        whileHover={{
          scale: 1.05,
        }}
        whileTap={{
          scale: 1,
          borderRadius: 20,
        }}
      >
        <Image
          className="z-30"
          src={require(`../results/${username}.png`)}
          width="450"
          height="450"
          layout="fixed"
        />
      </motion.div>
      <motion.div className="flex flex-col justify-between">
        <motion.div>
          <motion.h2 variants={item} className="text-4xl">
            Thème:
          </motion.h2>
          <motion.h1
            variants={item}
            className="mt-2 font-bold text-6xl bg-clip-text capitalize"
          >
            {theme}
          </motion.h1>
          <motion.h2 variants={item} className="text-4xl mt-5">
            Joueur:
          </motion.h2>
          <motion.h1
            variants={item}
            className="font-bold text-6xl mt-2 bg-clip-text"
          >
            {username}
          </motion.h1>
        </motion.div>
        <motion.div>
          <motion.div className="flex items-center">
            <motion.div>
              <StarIcon className="h-10" />
            </motion.div>
            <motion.h1 variants={item} className="text-4xl ml-2 font-extrabold">
              Pour noter le joueur ?
            </motion.h1>
          </motion.div>
          <motion.h2 variants={item} className="mt-2 text-xl w-96">
            Pour noter le joueur, il te suffit de revenir sur ton script Python
            et d'entrer une note entre 0 et 10 compris!
          </motion.h2>
        </motion.div>

        {/* <motion.div>
          <motion.h2 variants={item} className="text-4xl mb-4">
            Notes:
          </motion.h2>
          <motion.div variants={item} className="flex items-center flex-grow">
            <VoteButtons
              text="🤮 Beurk"
              color="red-600"
              selected={selected}
              setSelected={setSelected}
              int={"1"}
            />
            <VoteButtons
              text="😪 Mauvais"
              color="yellow-400"
              selected={selected}
              setSelected={setSelected}
              int={"2"}
            />
            <VoteButtons
              text="😅 Ça passe"
              color="yellow-300"
              selected={selected}
              setSelected={setSelected}
              int={"3"}
            />
            <VoteButtons
              text="🙂 Bien"
              color="green-400"
              selected={selected}
              setSelected={setSelected}
              int={"4"}
            />
            <VoteButtons
              text="😁 Très bien"
              color="blue-400"
              selected={selected}
              setSelected={setSelected}
              int={"5"}
            />
            <VoteButtons
              text="😳 WOOOW"
              color="indigo-700"
              selected={selected}
              setSelected={setSelected}
              int={"6"}
            />
          </motion.div>
        </motion.div> */}
      </motion.div>
      <Toaster />
    </motion.div>
  );
};

export default ResultComponent;
