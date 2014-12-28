"""
Schema:

github_users:
{
  _id: <objectid>,
  extid: <int>,
  url: <str>,
  login: <str>,
  follwers: [<str>],
  follwers_count: <int>,
  follwing: [<str>],
  follwing_count: <int>,
  type: <str>,
  name: <str>,
  company: <str>,
  blog: <str>,
  location: <str>,
  email: <str>
}

github_repos:
{
  _id: <objectid>,
  extid: <int>,
  url: <str>,
  fullname: <str>,
  langs: [<str>],
  readme: <str>,
  homepage: <str>,
  descr: <str>,
  stars_count: <int>,
  forks_count: <int>,
  commits_count: <int>,
  contributors_count: <int>,
  tags: [<str>]
}
"""
