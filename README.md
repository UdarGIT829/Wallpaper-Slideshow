# Wallpaper Slideshow for Linux

This is a program I developed for personal use, as programs like Nitrogen that are generally used to slideshow through wallpapers do not have any intelligence to them as far as determining which image to display.

## Motivation
I decided on a whim to develop a simple wallpaper slideshow program to practice in the Ruby Language, however I was alarmed one night when the wallpaper changed to a bright image that assaulted my sleepy eyes with white light. After some thought I set about to select only dark images for display at night time, and the other images would be allowed to be displayed during day time.



I already had some experience analyzing colors in Python for a project in a class, whereby clothing would be chosen based on its color to "match" with other pieces of clothing resulting in a outfit. Additionally in a project for another class my group had tried to create our own rendition of K-means clustering to analyze images, however the program was quite cumbersome and ran into a logistical hitch that we, nor our professor, could not debug. Regardless, with these experiences in mind I set about to analyze each image in my wallpaper folder prior to displaying them as a wallpaper. 

## Planning
As my experience with image analysis was in Python, and because it was on a very elementary level, I wanted to use Python to analyze the images. As I mentioned earlier I wanted to use Ruby to select the wallpaper randomly and ensure that it was dark enough if it was night time. However if I were to analyze any image everytime it got randomly chosen, I would likely be doing the analysis more than once, which was undesired. Additionally, I was worried that analysing each pixel of every image would be cumbersome, so I wanted to try using clustering to hopefully minimize the amount of computations per image. 

I decided to use cv2 to analyze images, as it had a kmeans function to analyze images that I would first use to analyze images. Finally I decided upon a threshold of 50% brightness, or RGB of (127,127,127), and the divide between whether an image would be considered bright or dark.

After implementing some small parts such as time recognition, executing Linux shell commands from Ruby code, and analysing images for brightness using cv2's kmeans function, I decided to write out my plan algorithmically on pen & paper to ensure it would be as efficient as possible.

## Algorithmic analysis
As mentioned before I did not want to analyse each image upon random selection; to this end I was about to confirm through big-O notation of the algorithms in place that in order to display any image using that method, the worst case situation result in O(n^2) time. Alternatively if I were to analyse each image once and store the result into an appropriate file for day and night respectively, the algorithm that randomly selects an image from the file pertaining to the time of day, would take about O(1) time or a constant amount of time regardless of the amount of images being considered.

## Implementation
The first thing I noticed after implementing this program was that the images that were considered as "dark" might have a wide swath of white in the image that would only get recognized as a single cluster, regardless of it's size relative to the image. Additionally, the K-means clustering function was a bit slow and I wasn't sure how to speed it up. Instead of K-means I switched over to scanning each pixel and taking the average amount of brightness of all pixels to determine whether the image was dark or not. This resulted in a 5 times speed up, and I will be keeping this change in particular. 

Recently it came to my attention that images that contained a sizeable amount of bright colors might still easily be considered as a dark image, so I will plan to gather an accurate ratio of pixels such that, for example if 25% of pixels are bright white color that the image would no longer be eligible as a dark image. 