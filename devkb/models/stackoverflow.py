"""
Schema:

stackoverflow_users:
{
  _id: <objectid>,
  extid: <int>,
  url: <str>,
  name: <str>,
  reputation: <int>,
  tags: [<str>]
}

stackoverflow_tags:
{
  _id: <objectid>,
  url: <str>,
  name: <str>,
  qcount: <int>,
  descr: <str>
}

stackoverflow_questions:
{
  _id: <objectid>,
  url: <str>,
  title: <str>,
  body: <str>,
  tags: [<str>],
  vote: <int>,
  comments: [<str>],
  user_id: <int>,
  answers: [
    {
      extid: <int>,
      url: <str>,
      body: <str>,
      vote: <int>,
      accept: <bool>,
      comments: [<str>],
      user_id: <int>
    }
  ]
}
"""
