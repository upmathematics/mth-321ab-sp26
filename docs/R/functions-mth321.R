library(tidyverse)
library(gridExtra)
library(latex2exp)

# vector/slope field for one ode
SlopeField <- function(FUN,params=c(),
                       tlim=c(-1,1),ylim=c(-1,1),res=10,
                       scale=0.10,radius=0.5,unit=FALSE,
                       col="black",xlab="t",ylab="y",title=""){
  
  # variables
  t_var <- seq(tlim[1],tlim[2],length.out=res)
  y_var <- seq(ylim[1],ylim[2],length.out=res)
  ty_mesh <- expand_grid(t_var,y_var)
  t_diff <- t_var[2]-t_var[1]
  
  # apply ode function and create vector points
  vector_points <- ty_mesh %>% 
    mutate(slope = FUN(t_var,y_var,params)[[1]],
           t_0_orig = t_var,
           y_0_orig = y_var,
           t_1_orig = t_0_orig+t_diff*scale,
           y_1_orig = y_0_orig+slope*t_diff*scale,
           t_midpoint = (t_1_orig-t_0_orig)/2,
           y_midpoint = (y_1_orig-y_0_orig)/2,
           norm = sqrt((t_1_orig-t_0_orig)^2 + (y_1_orig-y_0_orig)^2),
           unit_t = scale*(t_1_orig-t_0_orig)/norm,
           unit_y = scale*(y_1_orig-y_0_orig)/norm,
           unit_t_midpoint = unit_t/2,
           unit_y_midpoint = unit_y/2,
           t_0 = case_when(
               unit == TRUE ~ t_0_orig-unit_t_midpoint,
               unit == FALSE ~ t_0_orig-t_midpoint
             ),
           y_0 = case_when(
             unit == TRUE ~ y_0_orig-unit_y_midpoint,
             unit == FALSE ~ y_0_orig-y_midpoint
           ),
           t_1 = case_when(
             unit == TRUE ~ t_0_orig+unit_t-unit_t_midpoint,
             unit == FALSE ~ t_1_orig-t_midpoint
           ),
           y_1 = case_when(
             unit == TRUE ~ y_0_orig+unit_y-unit_y_midpoint,
             unit == FALSE ~ y_1_orig-y_midpoint
           ))
  
  # draw slope field
  ggplot(data=vector_points) +
    geom_hline(yintercept=0, color="darkgray") + 
    geom_vline(xintercept=0, color="darkgray") +
    geom_segment(aes(x=t_0, y=y_0, xend=t_1, yend=y_1),
                 color=col,
                 arrow = arrow(length = unit(scale*radius, "inches"))) + 
    labs(x=xlab,y=ylab)+
    ggtitle(title) +
    theme_minimal()
}

# Vector field / phase portrait for system of two odes
PhasePortrait <- function(FUN,params=c(),
                          xlim=c(-1,1),ylim=c(-1,1),res=10,
                          scale=0.10,radius=0.5,unit=FALSE,axis=TRUE,
                          col="black",xlab="x",ylab="y",title=""){
  
  # variables
  x_var <- seq(xlim[1],xlim[2],length.out=res)
  y_var <- seq(ylim[1],ylim[2],length.out=res)
  xy_mesh <- expand_grid(x_var,y_var)
  
  # apply ode function and create vector points
  ode_points <- xy_mesh %>% 
    mutate(dx = FUN(x_var,y_var,params)[[1]],
           dy = FUN(x_var,y_var,params)[[2]],
           x_0_orig = x_var,
           y_0_orig = y_var,
           x_1_orig = x_var+dx*scale,
           y_1_orig = y_var+dy*scale,
           x_midpoint = (x_1_orig-x_0_orig)/2,
           y_midpoint = (y_1_orig-y_0_orig)/2,
           norm = sqrt((x_1_orig-x_0_orig)^2 + (y_1_orig-y_0_orig)^2),
           unit_x = scale*(x_1_orig-x_0_orig)/norm,
           unit_y = scale*(y_1_orig-y_0_orig)/norm,
           unit_x_midpoint = unit_x/2,
           unit_y_midpoint = unit_y/2,
           x_0 = case_when(
             unit == TRUE ~ x_0_orig-unit_x_midpoint,
             unit == FALSE ~ x_0_orig-x_midpoint
           ),
           y_0 = case_when(
             unit == TRUE ~ y_0_orig-unit_y_midpoint,
             unit == FALSE ~ y_0_orig-y_midpoint
           ),
           x_1 = case_when(
             unit == TRUE ~ x_0_orig+unit_x-unit_x_midpoint,
             unit == FALSE ~ x_1_orig-x_midpoint
           ),
           y_1 = case_when(
             unit == TRUE ~ y_0_orig+unit_y-unit_y_midpoint,
             unit == FALSE ~ y_1_orig-y_midpoint
           ))
  
  # draw slope field
  p <- ggplot(data=ode_points)
  
  if (axis == TRUE){
    p <- p + 
      geom_hline(yintercept=0, color="darkgray") + 
      geom_vline(xintercept=0, color="darkgray")
  } else if (axis == FALSE){
    p <- p
  }
  
  p <- p + 
    geom_segment(aes(x=x_0, y=y_0, xend=x_1, yend=y_1),
                 color=col,
                 arrow = arrow(length = unit(scale*radius, "inches"))) + 
    labs(x=xlab,y=ylab)+
    ggtitle(title) +
    theme_minimal()
  
  p
}