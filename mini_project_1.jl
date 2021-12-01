# Mini-project 1 for Modern Algorithmic Toolbox
# This assignment is not complete; I was learning Julia at 
# the same time and decided it was a bad idea, opting for Python instead
# uniform random distribution
import Random: MersenneTwister
rng = MersenneTwister()

using Plots

# Select one of the N bins uniformly at random, and place the current ball in it 
function choosebin1(N, bins)
    rand(rng, 1:N)
end

# Select two of the N bins uniformly at random (either with or without replacement), and look at how
# many balls are already in each. If one bin has strictly fewer balls than the other, place the current ball
# in that bin. If both bins have the same number of balls, pick one of the two at random and place the
# current ball in it.
function choosebin2(N, bins)
    bin1 = choosebin1(N, bins)
    bin2 = choosebin1(N, bins)
    
    if bins[bin1] < bins[bin2]
        return bin1
    elseif bins[bin2] < bins[bin1]
        return bin2
    else
        if rand(Bool)
            bin1
        else
            bin2
        end
    end
end

#  Same as the previous strategy, except choosing three bins at random rather than two.
function choosebin3(N, bins)
    bin1 = choosebin1(N, bins)
    bin2 = choosebin1(N, bins)
    bin3 = choosebin1(N, bins)
    
    min = bins[bin1]
    minbin = bin1
    
    if bins[bin2] < min
        min = bins[bin2]
        minbin = bin2
    end
    
    if bins[bin3] < min
        minbin = bin3
    end
    
    minbin
end

# Select two bins as follows: the first bin is selected uniformly from the first N/2 bins, and the second
# uniformly from the last N/2 bins. (You can assume that N is even.) If one bin has strictly fewer balls
# than the other, place the current ball in that bin. If both bins have the same number of balls, place
# the current ball (deterministically) in the first of the two bins.
function choosebin4(N, bins)
    halfN = N ÷ 2
    bin1 = choosebin1(halfN, bins)
    bin2 = choosebin1(halfN, bins) + halfN
    
    bin1size = bins[bin1]
    bin2size = bins[bin2]
    if bin1size < bin2size
        bin1
    elseif bin2size < bin1size
        bin2
    else
        bin1
    end
end

# Toss N balls into N bins, choosing the bin using the binchooser function
# Return the maximum number of balls in any bin
function balltoss(N, binchooser)
    bins = zeros(UInt32, N)
    max = 0
    
    let balls = N
        while balls > 0
            balls -= 1
            bin = binchooser(N, bins)
            bins[bin] += 1
            
            if bins[bin] > max
                max = bins[bin]
            end
        end
    end
    
    return max
end

balltoss(10, choosebin1)

balltoss(10, choosebin2)

balltoss(10, choosebin3)

balltoss(10, choosebin4)

function simulate(binchooser)
    maxvalues = []
    N = 200_000
    let r = 100
        while r > 0
            push!(maxvalues, balltoss(N, binchooser))
            r -= 1
        end
    end
    maxvalues
end

maxvalues1 = simulate(choosebin1)
maxvalues2 = simulate(choosebin2)
maxvalues3 = simulate(choosebin3)
maxvalues4 = simulate(choosebin4)

histogram(maxvalues1, bins=5:12, label="Method 1")

histogram(maxvalues2, bins=1:8, label="Method 2")

histogram(maxvalues3, bins=1:6, label="Method 3")

histogram(maxvalues4, bins=1:6, label="Method 4")
