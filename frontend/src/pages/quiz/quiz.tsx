import React from 'react';
import { useParams } from 'react-router-dom';
import Quiz from '../../components/quiz/Quiz';

const QuizPage = () => {
    const { quizId } = useParams<{ quizId: string }>();

    return (
        <div>
            <h1>Quiz {quizId}</h1>
            <Quiz quizId={Number(quizId)} />
        </div>
    );
};

export default QuizPage;
