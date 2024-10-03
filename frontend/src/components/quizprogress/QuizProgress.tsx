import React from 'react';

type QuizProgressProps = {
    totalQuestions: number;
    currentProgress: string;
    score: number;
};

const QuizProgress = ({ totalQuestions, currentProgress, score }: QuizProgressProps) => {
    return (
        <div>
            <p>Progress: {currentProgress}</p>
            <p>Score: {score}</p>
            <p>Total Questions: {totalQuestions}</p>
        </div>
    );
};

export default QuizProgress;
