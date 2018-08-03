var fs = require('fs');
var express = require('express');
var graphqlHTTP = require('express-graphql');
var { buildSchema } = require('graphql');
const { makeExecutableSchema } = require('graphql-tools');
const { resolvers } = require('./graphql-resolvers');
const typeDefs = fs.readFileSync('schema.graphql').toString();

const schema = makeExecutableSchema({typeDefs, resolvers});

const { Client } = require('pg')

const client = new Client({
    database: 'unigator',
    user: 'unigator'
});

async function connectDB() {
    await client.connect();
    return client;
}

var app = express();

connectDB().then(function(db){

    app.use('/graphql', graphqlHTTP({
      schema,
      graphiql: true,
      context: {login: 12345, db}
    }));

    app.listen(4000, () => console.log('Now browse to localhost:4000/graphql'));
})
