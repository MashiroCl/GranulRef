#!/usr/bin/ruby

input_file = ARGV.shift
lines = IO.readlines(input_file).select {|l| l.start_with?("pick") }
lines = lines.map {|l| id,
msg = l.scan(/^pick (\w+) (.*)/)[0] ;
                       { :line => l, :id => id, :msg => msg } }

cluster_info_file = ENV["CC_CLUSTER_INFO"] || "cc_cluster_info.txt"
cluster_targets = File.readlines(cluster_info_file).map {|l| l.chomp }

File.open(input_file, "w") do |f|
  f.puts "pick #{lines[0][:id]} #{lines[0][:msg]}"
  puts "pick #{lines[0][:id]} #{lines[0][:msg]}"
  lines[1..-1].each do |e|
    if (cluster_targets.find{|temp|/#{e[:id]}/=~temp})!=nil
      f.puts "squash #{e[:id]} #{e[:msg]}"
      puts "squash #{e[:id]} #{e[:msg]}"
    else
      f.puts "drop #{e[:id]} #{e[:msg]}"
      puts "drop #{e[:id]} #{e[:msg]}"
    end
  end
end