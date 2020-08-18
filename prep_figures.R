# outputs rectangle
png1 <- grid::rasterGrob(as.raster(png::readPNG("figures/rectangle_5_3_out_mean.png")),
                         interpolate = TRUE)
png1 <- gridExtra::arrangeGrob(png1, bottom = "(a)")

  png2<- grid::rasterGrob(as.raster(png::readPNG("figures/rectangle_5_3_out_max.png")),
                        interpolate = T)
png2 <- gridExtra::arrangeGrob(png2, bottom = "(b)")

png3 <- grid::rasterGrob(as.raster(png::readPNG("figures/rectangle_5_3_out_std.png")),
                         interpolate = T)
png3 <- gridExtra::arrangeGrob(png3, bottom = "(c)")



png("figures/rectangle.png", width = 24, height = 10, res = 400, units = "cm")
gridExtra::grid.arrange(png1, png2, png3, nrow = 1)
dev.off()

# outputs circle
png1 <- grid::rasterGrob(as.raster(png::readPNG("figures/circle_3_out_mean.png")),
                         interpolate = TRUE)
png1 <- gridExtra::arrangeGrob(png1, bottom = "(a)")

png2<- grid::rasterGrob(as.raster(png::readPNG("figures/circle_3_out_max.png")),
                        interpolate = T)
png2 <- gridExtra::arrangeGrob(png2, bottom = "(b)")

png3 <- grid::rasterGrob(as.raster(png::readPNG("figures/circle_3_out_std.png")),
                         interpolate = T)
png3 <- gridExtra::arrangeGrob(png3, bottom = "(c)")



png("figures/circle.png", width = 24, height = 10, res = 400, units = "cm")
gridExtra::grid.arrange(png1, png2, png3, nrow = 1)
dev.off()

# outputs rectangle
png1 <- grid::rasterGrob(as.raster(png::readPNG("figures/wedge_3_0_135_out_mean.png")),
                         interpolate = TRUE)
png1 <- gridExtra::arrangeGrob(png1, bottom = "(a)")

png2<- grid::rasterGrob(as.raster(png::readPNG("figures/wedge_3_0_135_out_max.png")),
                        interpolate = T)
png2 <- gridExtra::arrangeGrob(png2, bottom = "(b)")

png3 <- grid::rasterGrob(as.raster(png::readPNG("figures/wedge_3_0_135_out_std.png")),
                         interpolate = T)
png3 <- gridExtra::arrangeGrob(png3, bottom = "(c)")



png("figures/wedge.png", width = 24, height = 10, res = 400, units = "cm")
gridExtra::grid.arrange(png1, png2, png3, nrow = 1)
dev.off()



# windows
png1 <- grid::rasterGrob(as.raster(png::readPNG("figures/rectangle_5_3_out_window.png")),
                         interpolate = TRUE)
png1 <- gridExtra::arrangeGrob(png1, bottom = "(a)")

png2<- grid::rasterGrob(as.raster(png::readPNG("figures/circle_3_out_window.png")),
                         interpolate = T)
png2 <- gridExtra::arrangeGrob(png2, bottom = "(b)")

png3 <- grid::rasterGrob(as.raster(png::readPNG("figures/wedge_3_0_135_out_window.png")),
                         interpolate = T)
png3 <- gridExtra::arrangeGrob(png3, bottom = "(c)")



png("figures/windows.png", width = 24, height = 10, res = 400, units = "cm")
gridExtra::grid.arrange(png1, png2, png3, nrow = 1)
dev.off()
