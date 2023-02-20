require 'sinatra'
require 'mysql2'
require 'securerandom'

set :bind, '0.0.0.0'
set :port, 80
set :public_folder, 'static'

enable :sessions

$flag = ENV["FLAG"]

$client = Mysql2::Client.new(
  :host => ENV["DB_HOST"],
  :username => ENV["DB_USERNAME"],
  :password => ENV["DB_PASSWORD"],
  :database => ENV["DB_DATABASE"]
)

$client.query(
  "CREATE TABLE IF NOT EXISTS `users` (
    `id` INT unsigned NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(63) NOT NULL,
    `password` VARCHAR(63) NOT NULL,
    `is_admin` BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
  );"
)

get '/' do
  if session[:username] then
    @username = session[:username]
    erb :index
  else
    redirect '/login.html'
  end
end

post '/admin/init' do
  username = "admin-#{SecureRandom.hex}"
  password = SecureRandom.hex
  statement = $client.prepare("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)")
  statement.execute(username, password, 1)
  return "{\"username\":\"#{username}\"}"
end

post '/register' do
  begin
    statement = $client.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
    result = statement.execute(params[:username], params[:password])
    redirect 'login.html'
  rescue Error
    redirect 'register.html?error'
  end
end

def is_admin(username)
  statement = $client.prepare("SELECT is_admin FROM users WHERE username=? LIMIT 1")
  is_admin_result = statement.execute(username)
  return is_admin_result.first["is_admin"]==1 ? true : false
end

def check_login(username, password)
  statement = $client.prepare("SELECT id FROM users WHERE username=? and password=? ORDER BY id DESC LIMIT 1")
  result = statement.execute(username, password)
  return result.count > 0
end

post '/login' do
  username = params[:username]
  password = params[:password]

  if check_login username, password then
    session[:username] = username
    session[:is_admin] = is_admin username
    redirect ''
  else
    redirect 'login.html?error'
  end
end
