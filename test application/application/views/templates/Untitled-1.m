X = [1,1;1,2;2,1;0,0;1,0;0,1];
y = [0,0,0,1,1,1];
y = y';

SVMModel = fitcsvm(X,y,'KernelFunction','linear','ClassNames',{'0','1'});

rng(1); % For reproducibility
[SVMModel,ScoreParameters] = fitPosterior(SVMModel,'Holdout',0.8); 

xMax = max(X);
xMin = min(X);
d = 0.01;
[x1Grid,x2Grid] = meshgrid(xMin(1):d:xMax(1),xMin(2):d:xMax(2));

[~,PosteriorRegion] = predict(SVMModel,[x1Grid(:),x2Grid(:)]);

figure;
contourf(x1Grid,x2Grid,...
        reshape(PosteriorRegion(:,2),size(x1Grid,1),size(x1Grid,2)));
h = colorbar;
h.Label.String = 'P({\it{versicolor}})';
h.YLabel.FontSize = 16;
caxis([0 1]);
colormap jet;

hold on
h2 = gscatter(X(:,1),X(:,2),y,'mb','*x',[15,10]);
set(h2, 'LineWidth', 2, 'MarkerSize',10);
sv = X(SVMModel.IsSupportVector,:);
plot(sv(:,1),sv(:,2),'yo','MarkerSize',19,'LineWidth',3);
axis tight
grid on