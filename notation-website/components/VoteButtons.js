import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { motion } from "framer-motion";

const VoteButtons = ({ color, text, selected, setSelected, int }) => {
  const [colors, setColors] = useState(color);

  useEffect(() => {
    setColors(color);
  }, []);

  const buttonStyle = `bg-${color} text-white select-none ${
    selected === int ? "shadow-xl" : "shadow-lg"
  } mx-5 cursor-pointer font-title font-semibold flex justify-center w-28 h-16 items-center rounded-xl transition-all transform hover:scale-110`;

  return (
    <motion.div
      initial={{ scale: 1 }}
      animate={selected === int ? { scale: 1.3 } : { scale: 1 }}
      whileHover={{ scale: 1.3 }}
      whileTap={{ scale: 1.1 }}
      className={`${buttonStyle}`}
      onClick={() => {
        setSelected(int);
        console.log(selected);
        console.log(int);
        toast.success(`Tu as voté pour: ${text}`, {
          position: "top-right",
        });
      }}
    >
      <h1 className="text-xs">{text}</h1>
    </motion.div>
  );
};

export default VoteButtons;
