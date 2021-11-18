import React, { useState, useEffect } from "react";

import { motion } from "framer-motion";

const Header = (props) => {
  const [seconds, setSeconds] = useState(props.time);

  if (seconds === -1) {
    setSeconds(props.time);
  }

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((seconds) => seconds - 1);
    }, 1000);
  }, []);

  const headerVariant = {
    hidden: {
      y: -150,
      opacity: 0,
    },
    show: {
      y: 0,
      opacity: 1,
      transition: {
        type: "string",
        bounce: 0,
        duration: 1,
        // when: "beforeChildren",
        staggerChildren: 0.15,
        delayChildren: 0.7,
      },
    },
  };

  const item = {
    hidden: {
      y: 17,
      opacity: 0,
    },
    show: {
      y: 0,
      opacity: 1,
      transition: {
        type: "tween",
        // bounce: 0,
        duration: 0.35,
      },
    },
    exit: {
      x: -100,
      opacity: 0,
    },
  };

  return (
    <motion.div
      variants={headerVariant}
      initial="hidden"
      animate="show"
      className="flex flex-col items-center p-5 shadow-xl sticky top-0 bg-white z-40"
    >
      <motion.h1 variants={item} className="text-8xl font-title font-semibold">
        DrawBattle
      </motion.h1>
      {props.end === 0 ? (
        <motion.p>
          Vous avez{" "}
          <span
            className={seconds <= 10 ? "font-bold text-red-500" : "font-bold"}
          >
            {seconds} secondes
          </span>{" "}
          pour voter cette composition!
        </motion.p>
      ) : (
        <motion.p variants={item}>
          Tous les compositions de chacun ont reçu une{" "}
          <span className="font-bold">note</span> de la part de chacun des
          joueurs !
        </motion.p>
      )}
    </motion.div>
  );
};

export default Header;
