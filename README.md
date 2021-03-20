# BeautifulKuskus

A minimal framework to extract content from HTML with BeautifulSoup and scikit-learn.

## Basic usage
    from beatifulkuskus import BeautifulKuskus

    html="""
    <html><body>
    <h1>Header</h1>
    <div id="content">
    Ba <span class="a b c">boom</span>
    </div>
    <h5>Footer</h5>
    </body></html>
    """
    def id_is_content(x):
        return "content" in x.ids
    kuskus = BeautifulKuskus(html)
    print(str(kuskus.prune_by_func(id_is_content)))
    
## SKlearn Model usage
    from beatifulkuskus import BeautifulKuskus, DataPoint
    import joblib # or any other model serialization format

    def preprocess(data:DataPoint)->str:
        """This model would only consider the class names and ids"""
        # data is ("element", "tags", "classes", "ids", "text")
        classes = [" ".join(class_list) class_list for class_list on data.classes]
        return " ".join(data.ids) + " " + " ".join(classes)

    model = joblib.load("content_model_on_ids_and_classes.joblib")
    kuskus = BeautifulKuskus(html)
    kuskus.prune_by_content_model(model, preprocess=preprocess)
    
