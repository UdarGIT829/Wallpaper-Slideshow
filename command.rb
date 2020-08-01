arguement = ARGV
require 'digest'

working_dir = ARGV[0]
p working_dir

def check_last_wall(im, working_dir)
  last_wallpaper=`cat /home/vudar/.fehbg`
  last_wallpaper = last_wallpaper.split(' ')[3]
  last_wallpaper.gsub! "'", ""  
  while im.include? last_wallpaper
    p "New wall is same!"
    im = randomImageFinder(working_dir)
  end  
  return im
end


def check_if_night()
  time_call = IO.popen("date +%H")
  hour_is = time_call.readlines[0].gsub!(/[^0-9A-Za-z]/, '').to_i
  if hour_is > 19 || hour_is < 8
    p "is night"
    return true
  else
    p "not night"
    return false
  end #fi
  time_call.close
end #endFunction

def randomImageFinder(working_dir)
  #Check time for night or day
  check_in = working_dir.dup
  if check_if_night
    check_in << 'dImages.txt'
  else
    check_in << 'lImages.txt'
  end #fi
  files = Array.new
  begin
    File.foreach(check_in) {|line| files.push(line)}
    files.each do |file|
      if file.include?(".sh") || file.include?(".rb") || file.include?(".txt") || file.include?(".py")
        files.delete($file)
      end #fi
    end #endWhile
    alternatives = files.size
    p alternatives
    return [files[rand(files.size)], alternatives]
  rescue
    return "NO FILE FOUND"
  end
end #endFunction


randomImage = randomImageFinder(working_dir)
if randomImage[0] == "NO FILE FOUND"
  p "Run imageAnalyzer.py before executing this program"
elsif randomImage[1] == 1
  path_to_image = randomImage[0]
else
  path_to_image = check_last_wall(randomImage, working_dir)
end #fi
p "feh --bg-center #{path_to_image}"
exec("DISPLAY=:0 feh --bg-center #{path_to_image}")
