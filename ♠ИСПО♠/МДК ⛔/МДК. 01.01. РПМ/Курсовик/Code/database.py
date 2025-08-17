from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///bot.db')
Session = sessionmaker(bind=engine)

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    questions = relationship('Question', back_populates='test')

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    test_id = Column(Integer, ForeignKey('tests.id'))
    test = relationship('Test', back_populates='questions')
    answers = relationship('Answer', back_populates='question')

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', back_populates='answers')

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    test_id = Column(Integer)
    score = Column(Integer)

Base.metadata.create_all(engine)